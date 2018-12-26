from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import Shift, ShiftDetails, User
import sys
from math import floor

shifts = Blueprint('shifts', __name__)

@shifts.route('/add_shifts')
@login_required
def add_shifts():
    print(current_user.email == "")

    

@shifts.route('/drop_shifts')
def drop_shifts():
    shift_details = ShiftDetails.query.filter_by(tutor_id = current_user.id).all()
    user = current_user
    shifts_s = []
    shifts_f = []
    for detail in shift_details:
        print(detail.id)
        shift = Shift.query.filter_by(id = detail.shift_id).first()
        print(type(shift))
        if isinstance(shift.start, float):
            shift_f = str(shift.end) + ":00"
            shift = (str(floor(shift.start))+ ":30")
        else:
            shift_f = str(floor(shift.end)) + ":30"
            shift = str(shift.start) + ":00"
        shifts_s.append(shift)
        shifts_f.append(shift_f)
        store = zip(shifts_s, shifts_f)
    return render_template('shifts/drop_shifts.html', **locals())

@shifts.route('/release_shift')
def release_shift():
    pass

@shifts.route('/pickup_shift')
def pickup_shift():
    pass
#---------------------------------------------------------------------------
"""
shift_d = ShiftDetails(tutor_id = 2, shift_id = 4, status = 2)
        user.details.append(shift_d)
        db.session.add(user)
        db.session.commit()
"""
#---------------------------------------------------------------------------