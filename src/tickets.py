from flask import Blueprint, request

from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Ticket, db


tickets = Blueprint('tickets', __name__, url_prefix='/api/v1/tickets')


@tickets.route('/', methods=['GET'])
@jwt_required()
def all_tickets():
    """Returns all tickets of the board."""
    
    data = []
    tickets = Ticket.query.all()

    for ticket in tickets:
        data.append({
            'id': ticket.id,
            'body': ticket.body,
            'created_at': ticket.created_at,
            'updated_at': ticket.updated_at,
        })

    return {
        'tickets': data,
    }


@tickets.route('/', methods=['POST'])
@jwt_required()
def create_ticket():
    """
    Creates new ticket on the board.

    Receive post request containing body of ticket.
    """
    
    current_user = get_jwt_identity()

    body = request.json.get('body', '')

    if not body:
        return {
            'error': 'body field cat not be empty',
        }, 400

    ticket = Ticket(body=body, user_id=current_user)
    db.session.add(ticket)
    db.session.commit()

    return {
        'id': ticket.id,
        'body': ticket.body,
        'created_at': ticket.created_at,
    }, 201


@tickets.route('/<id>', methods=['PUT'])
@jwt_required()
def update_ticket(id):
    """
    Updates ticket on the board.

    Receive put request containing body of ticket.
    """

    current_user = get_jwt_identity()
    ticket = Ticket.query.get(id)

    if ticket.user_id != current_user:
        return {
            'error': 'You do not own this ticket',
        }, 403

    body = request.json.get('body', '')

    if not body:
        return {
            'error': 'body field can not be empty',
        }, 400

    ticket.body = body
    db.session.add(ticket)
    db.session.commit()

    return {
        'id': ticket.id,
        'body': ticket.body,
        'created_at': ticket.created_at,
        'updated_at': ticket.created_at,
    }, 200
