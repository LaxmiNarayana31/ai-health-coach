import logging
import traceback

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from google.genai import types

from app.models.user import User
from app.models.message import Message
from app.helper.llm_helper import gemini_llm_with_memory
from app.utils.loader import load_system_prompt
from app.services.protocol_service import ProtocolService
from app.services.history_service import HistoryService


class ChatService:
    @staticmethod
    async def init_chat(db: AsyncSession, user_id: int | None):
        try:
            if user_id:
                result = await db.execute(
                    select(Message).where(Message.user_id == user_id).order_by(Message.id.desc())
                )
                existing_message = result.scalars().first()
                if existing_message:
                    return existing_message, user_id

            # Create new user
            user = User()
            db.add(user)
            await db.commit()
            await db.refresh(user)

            # Simple greeting, let LLM take over for onboarding questions
            onboarding_text = "Hi! I'm Disha, your AI health coach 😊"

            message = Message(
                user_id=user.id,
                sender="assistant",
                content=onboarding_text
            )
            db.add(message)
            await db.commit()
            await db.refresh(message)

            return message, user.id
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            logging.error(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            logging.error(f"Exception occurred on line {line_no}")
            

    @staticmethod
    async def send_message(db: AsyncSession, user_id: int, user_message: str):
        try:
            # Save user message
            msg = Message(
                user_id=user_id,
                sender="user",
                content=user_message
            )
            db.add(msg)
            await db.commit()

            system_content = load_system_prompt()

            protocol_context = ProtocolService.get_relevant_protocols(user_message)
            if protocol_context:
                system_content += f"\n\n# PROTOCOL CONTEXT\nThe user seems to be describing a symptom or situation. Use the following medical protocols to guide your response if relevant:\n{protocol_context}"

            history_msgs_db = await HistoryService.get_context_messages(db, user_id, limit=10)
            
            contents = []
            for m in history_msgs_db:
                if m.id == msg.id:
                    continue
                
                role = "user" if m.sender == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": m.content}]
                })

            # Add current message
            contents.append({
                "role": "user",
                "parts": [{"text": user_message}]
            })

            try:
                llm = gemini_llm_with_memory(user_id)
                
                response = llm.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_content
                    )
                )
                
                # Check if response was blocked or empty
                if not response.text:
                    error_msg = "I'm sorry, I cannot respond to that message due to safety filters."
                    if response.candidates and response.candidates[0].finish_reason:
                        error_msg += f" (Reason: {response.candidates[0].finish_reason})"
                    
                    assistant_content = error_msg
                else:
                    assistant_content = response.text

            except Exception as e:
                # Handle all LLM errors gracefully so the chat doesn't crash
                logging.error(f"LLM Error: {str(e)}")
                
                # Default error message
                assistant_content = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
                
                # Check for specific Google GenAI errors if possible
                error_str = str(e).lower()
                if "429" in error_str or "quota" in error_str:
                    assistant_content = "Too many requests. Please try again in a moment."
                elif "400" in error_str or "key" in error_str:
                    assistant_content = "Technical error. Please try again in a moment."
                elif "safety" in error_str or "blocked" in error_str:
                    assistant_content = "I cannot answer that as it flagged my safety guidelines. Let's try asking something else."

            assistant_msg = Message(
                user_id=user_id,
                sender="assistant",
                content=assistant_content
            )
            db.add(assistant_msg)
            await db.commit()
            await db.refresh(assistant_msg)

            return assistant_msg
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            logging.error(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            logging.error(f"Exception occurred on line {line_no}")
