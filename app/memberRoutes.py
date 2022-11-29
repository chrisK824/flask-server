import json
from uuid import uuid4
import os
import sys
from datetime import datetime
import sqlalchemy
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from utils.utils import customResponse
from utils.defines import ErrorMessages as err
from utils.defines import Messages as msg
from app.schemas import Member
from app import app, db, member_schema, members_schema


@app.route('/members', methods=['GET', 'POST'])
def GetPostMembers():
    if request.method == 'GET':
        members = Member.query.all()
        return customResponse(members_schema.dump(members))
    elif request.method == 'POST':
        # FIXME : Validate input for headers, fields and return 400 for bad requests
        post_data = request.get_json()
        new_member = Member(name=post_data['name'],
                            lastname=post_data['lastname'],
                            username=post_data['username'],
                            email=post_data['email'],
                            age=post_data['age'],
                            gender=post_data['gender'],
                            nationality=post_data['nationality'],
                            password=generate_password_hash(
                                post_data['password']),
                            registration_date=datetime.now(),
                            id=str(uuid4()),
                            active=True)

        if Member.query.filter_by(username=new_member.username).first():
            return customResponse(err.DUPLICATE.format('username', new_member.username), 403)
        elif Member.query.filter_by(email=new_member.email).first():
            return customResponse(err.DUPLICATE.format('email', new_member.email), 403)
        try:
            db.session.add(new_member)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return customResponse(err.INTEGRITY, 400)
        return customResponse(member_schema.dump(new_member))


@app.route('/members/<memberID>', methods=['GET', 'PUT', 'DELETE'])
def GetPutDeleteMember(memberID):
    member = Member.query.filter_by(id=memberID).first()
    if not member:
        return customResponse(err.NOT_FOUND.format('User'), 404)

    if request.method == 'GET':
        return customResponse(member_schema.dump(member))

    if request.method == 'DELETE':
        db.session.delete(member)
        db.session.commit()
        return customResponse(msg.DELETE_SUCCESS.format('User'))

    if request.method == 'PUT':
        post_data = request.get_json()
        # FIXME : Validate input for headers, fields and return 400 for bad requests
        if member.username != post_data['username'] and Member.query.filter_by(username=post_data['username']).first():
            return customResponse(err.DUPLICATE.format('username', post_data['username']), 403)
        elif member.email != post_data['email'] and Member.query.filter_by(email=post_data['email']).first():
            return customResponse(err.DUPLICATE.format('email', post_data['email']), 403)

        member.name = post_data['name']
        member.lastname = post_data['lastname']
        member.username = post_data['username']
        member.email = post_data['email']
        member.age = post_data['age']
        member.gender = post_data['gender']
        member.nationality = post_data['nationality']
        member.password = generate_password_hash(post_data['password'])
        member.registration_date = datetime.now()

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return customResponse(err.INTEGRITY, 400)

        return customResponse(member_schema.dump(member))


@app.route('/members/stats', methods=['GET'])
def GetMembersStats():
    oldest_registered, recently_registered = None, None

    oldest_registration = Member.query.with_entities(
        sqlalchemy.sql.func.min(Member.registration_date).label('max')).scalar()
    newest_registration = Member.query.with_entities(
        sqlalchemy.sql.func.max(Member.registration_date).label('min')).scalar()
    if oldest_registration:
        oldest_registered = Member.query.filter_by(
            registration_date=oldest_registration).first().id
    if newest_registration:
        recently_registered = Member.query.filter_by(
            registration_date=newest_registration).first().id

    avg_age = Member.query.with_entities(
        sqlalchemy.sql.func.avg(Member.age).label('average')).scalar()
    members_count = Member.query.count()
    males = Member.query.filter_by(gender='male').count()
    females = Member.query.filter_by(gender='female').count()
    stats = {
        "members_count": members_count,
        "avg_age": avg_age,
        "male": males,
        "female:": females,
        "Fan_Before_it_was_cool": oldest_registered,
        "Bandwagoner": recently_registered
    }

    return customResponse(stats)
