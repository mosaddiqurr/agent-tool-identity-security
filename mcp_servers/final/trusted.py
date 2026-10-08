from mcp.server import MCPServer


mcp = MCPServer("company.internal")


@mcp.tool()
def company_mail_send_email(
    recipient: str,
    message: str
) -> dict:
    """Source: company.internal. Company email connector."""

    return {
        "status": "SIMULATED_ONLY",
        "source": "company.internal",
        "recipient": recipient,
        "message": message,
        "sent": False
    }


if __name__ == "__main__":
    mcp.run()
