from __future__ import annotations


class RoleNavigation:
    """Defines the pages available to each authenticated role."""

    ADMIN = {
        "Analyze": [
            "Dashboard",
            "Cross-Domain Analytics",
            "Reports",
        ],
        "Customer Dashboards": [
            "Exercise Dashboard",
            "Health Dashboard",
            "Mental Wellness Dashboard",
            "Nutrition Dashboard",
        ],
        "Customer Data": [
            "Client Profiles",
            "User Accounts",
            "Exercise Entry",
            "Health Entry",
            "Mental Wellness Entry",
            "Nutrition Entry",
            "Blood Work",
            "Data Import",
            "Change Password",
            "Final Testing",
        ],
    }

    CLIENT = {
        "Customer Dashboards": [
            "Exercise Dashboard",
            "Health Dashboard",
            "Mental Wellness Dashboard",
            "Nutrition Dashboard",
        ],
        "Customer Data": [
            "Exercise Entry",
            "Health Entry",
            "Mental Wellness Entry",
            "Nutrition Entry",
            "Blood Work",
            "Change Password",
        ],
    }

    @classmethod
    def for_role(
        cls,
        role: str,
    ) -> dict[str, list[str]]:
        """Return a fresh navigation dictionary for the authenticated role."""

        source = (
            cls.ADMIN
            if role == "admin"
            else cls.CLIENT
        )

        return {
            category: list(pages)
            for category, pages in source.items()
        }

    @classmethod
    def is_allowed(
        cls,
        role: str,
        page: str,
    ) -> bool:
        """Return True when the requested page is permitted for the role."""

        navigation = cls.for_role(
            role
        )

        return any(
            page in pages
            for pages in navigation.values()
        )
