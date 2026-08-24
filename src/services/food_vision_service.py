from __future__ import annotations

import base64
import json
import re
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class FoodAnalysis:
    items: list[dict]
    estimated_total_quantity: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: str
    notes: str

    @property
    def item_summary(
        self,
    ) -> str:
        return "; ".join(
            (
                f"{item.get('food', 'Unknown food')} "
                f"({item.get('quantity', 'unknown quantity')})"
            )
            for item in self.items
        )


class FoodVisionService:
    """Optional AI food-photo analysis using an image-capable OpenAI model."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5.6-luna",
    ) -> None:
        if not api_key:
            raise ValueError(
                "An OpenAI API key is required."
            )

        self.client = OpenAI(
            api_key=api_key
        )
        self.model = model

    @staticmethod
    def _extract_json(
        text: str,
    ) -> dict:
        cleaned = text.strip()

        if cleaned.startswith(
            "```"
        ):
            cleaned = re.sub(
                r"^```(?:json)?\s*",
                "",
                cleaned,
            )
            cleaned = re.sub(
                r"\s*```$",
                "",
                cleaned,
            )

        return json.loads(
            cleaned
        )

    def analyze(
        self,
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
    ) -> FoodAnalysis:
        encoded = base64.b64encode(
            image_bytes
        ).decode("ascii")

        prompt = '''
Analyze this meal photo for a wellness-tracking application.

Return ONLY valid JSON with this exact structure:
{
  "items": [
    {
      "food": "string",
      "quantity": "string"
    }
  ],
  "estimated_total_quantity": "string",
  "calories": 0,
  "protein_g": 0,
  "carbs_g": 0,
  "fat_g": 0,
  "fiber_g": 0,
  "confidence": "low|medium|high",
  "notes": "string"
}

Estimate visible foods, approximate portions, and nutrition.
Be conservative. Do not claim exact nutrition from an image.
If an item or portion cannot be identified, say so in notes.
'''

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                        {
                            "type": "input_image",
                            "image_url": (
                                f"data:{mime_type};base64,{encoded}"
                            ),
                        },
                    ],
                }
            ],
        )

        payload = self._extract_json(
            response.output_text
        )

        return FoodAnalysis(
            items=list(
                payload.get(
                    "items",
                    [],
                )
            ),
            estimated_total_quantity=str(
                payload.get(
                    "estimated_total_quantity",
                    "Unknown",
                )
            ),
            calories=float(
                payload.get(
                    "calories",
                    0,
                )
            ),
            protein_g=float(
                payload.get(
                    "protein_g",
                    0,
                )
            ),
            carbs_g=float(
                payload.get(
                    "carbs_g",
                    0,
                )
            ),
            fat_g=float(
                payload.get(
                    "fat_g",
                    0,
                )
            ),
            fiber_g=float(
                payload.get(
                    "fiber_g",
                    0,
                )
            ),
            confidence=str(
                payload.get(
                    "confidence",
                    "low",
                )
            ),
            notes=str(
                payload.get(
                    "notes",
                    "",
                )
            ),
        )
