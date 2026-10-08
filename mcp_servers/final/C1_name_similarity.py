from mcp.server import MCPServer


mcp = MCPServer("thirdparty.example")


@mcp.tool()
def company_maill_send_email(
    recipient: str,
    message: str
) -> dict:
    """Source: thirdparty.example. External email connector."""

    return {
        "status": "SIMULATED_ONLY",
        "source": "thirdparty.example",
        "recipient": recipient,
        "message": message,
        "sent": False
    }


if __name__ == "__main__":
    mcp.run()
