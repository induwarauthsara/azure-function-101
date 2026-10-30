import azure.functions as func
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

TICKETS = {
    "AZ101-001": {
        "ticket_number": "AZ101-001",
        "attendee_name": "Alex Johnson",
        "email": "alex.johnson@example.com",
        "event": "Azure Functions 101",
        "ticket_type": "Standard",
        "status": "Registered",
    },
    "AZ101-002": {
        "ticket_number": "AZ101-002",
        "attendee_name": "Taylor Smith",
        "email": "taylor.smith@example.com",
        "event": "Azure Functions 101",
        "ticket_type": "Student",
        "status": "Registered",
    },
    "AZ101-003": {
        "ticket_number": "AZ101-003",
        "attendee_name": "Jordan Lee",
        "email": "jordan.lee@example.com",
        "event": "Azure Functions 101",
        "ticket_type": "Speaker",
        "status": "Registered",
    },
}


@app.route(route="az_vs_101")
def az_vs_101(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Ticket lookup request received.")

    ticket_number = req.params.get("ticket_number")
    if not ticket_number:
        try:
            request_body = req.get_json()
        except ValueError:
            request_body = {}
        ticket_number = request_body.get("ticket_number")

    if not ticket_number:
        return func.HttpResponse(
            '{"error": "Provide a ticket_number in the query string or JSON request body."}',
            status_code=400,
            mimetype="application/json",
        )

    ticket = TICKETS.get(ticket_number.upper())
    if not ticket:
        return func.HttpResponse(
            '{"error": "Ticket not found."}',
            status_code=404,
            mimetype="application/json",
        )

    return func.HttpResponse(
        body=json.dumps(ticket),
        status_code=200,
        mimetype="application/json",
    )