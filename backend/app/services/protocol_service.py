import traceback
import logging
from typing import List, Dict

class ProtocolService:
    # Basic keyword-based protocols (simplification of RAG)
    PROTOCOLS: Dict[str, str] = {
        "fever": (
            "PROTOCOL: FEVER/HIGH TEMPERATURE\n"
            "- Ask: How long? Exact temperature? Any chills or shivering?\n"
            "- Advise: Hydration, rest, light clothing.\n"
            "- Warning: If temp > 103F or lasts > 3 days, advise easy doctor consult."
        ),
        "headache": (
            "PROTOCOL: HEADACHE\n"
            "- Ask: Location (front/back)? Intensity (1-10)? Sensitivity to light?\n"
            "- Advise: Rest in dark room, hydration, less screen time.\n"
            "- Warning: If sudden severe pain or vision changes, advise immediate help."
        ),
        "stomach": (
            "PROTOCOL: STOMACH PAIN/ISSUES\n"
            "- Ask: Sharp or dull? When did it start? Any food triggers?\n"
            "- Advise: Light bland food, hydration (ORS if loose motion).\n"
            "- Warning: If severe pain or blood in stool, see doctor."
        ),
        "cold": (
            "PROTOCOL: COLD/COUGH\n"
            "- Ask: Dry or wet cough? Sore throat? Runny nose?\n"
            "- Advise: Warm water gargle, steam inhalation, honey+ginger.\n"
            "- Warning: If breathing difficulty, advise doctor immediately."
        ),
        "refund": (
            "PROTOCOL: REFUND POLICY\n"
            "- Standard: Refunds only processed within 7 days of purchase if service not used.\n"
            "- Contact: Email support@cure.link for processing."
        )
    }

    @staticmethod
    def get_relevant_protocols(message: str) -> str:
        try:
            """
            Scans message for keywords and returns relevant protocol texts.
            """
            message_lower = message.lower()
            matched_protocols = []

            for keyword, protocol_text in ProtocolService.PROTOCOLS.items():
                if keyword in message_lower:
                    matched_protocols.append(protocol_text)
            
            # Also check for synonym "temperature" for fever
            if "temperature" in message_lower and "fever" not in message_lower:
                matched_protocols.append(ProtocolService.PROTOCOLS["fever"])

            # Synonym for stomach
            if "belly" in message_lower or "abdomen" in message_lower:
                if "stomach" not in message_lower:
                    matched_protocols.append(ProtocolService.PROTOCOLS["stomach"])

            if not matched_protocols:
                return ""

            return "\n\n".join(matched_protocols)
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            logging.error(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            logging.error(f"Exception occurred on line {line_no}")
