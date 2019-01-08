from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Shift, ShiftDetails, User
from app.shifts.forms import DropForm
import sys, time
from math import floor
from app.shifts.store import Shift_Enum

shifts = Blueprint('shifts', __name__)

@shifts.route('/add_shifts')
@login_required
def add_shifts():
    #prevent duplicates
    print(current_user.email == "")

@shifts.route('/drop_shifts', methods = ['GET', 'POST'])
def drop_shifts():

    def translate_time(shift):
        shift_start = shift[0]
        shift_start = time.strptime(shift_start, "%H:%M")
        shift_end = shift[1]
        shift_end = time.strptime(shift_end, "%H:%M")
        return (shift_start.tm_hour + (0.5 if shift_start.tm_min == 30 else 0), shift_end.tm_hour + (0.5 if shift_end.tm_min == 30 else 0))

    shift_details = ShiftDetails.query.filter_by(tutor_id = current_user.id).all()
    user = current_user
    shifts_s = []
    shifts_f = []
    form = DropForm()

    for detail in shift_details:
        if detail.status != Shift_Enum.ASSIGNED.value:
            continue

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
    #print([translate_time(item) for item in store])
    
    print("id", user.id)
    if form.validate_on_submit():
        user = current_user
        
        if user is not None:
            
            
            shift = Shift.query.filter_by(start = 1).first().id
            save = ShiftDetails.query.filter_by(tutor_id = user.id, shift_id = shift).first()
            print(save.status)
            save.status = 4
            db.session.commit()
            #add validation for legal shift
            
        return redirect(url_for('shifts.drop_shifts'))

    return render_template('shifts/drop_shifts.html', **locals())

@shifts.route('/release_shift')
def release_shift():
    pass


@shifts.route('/pickup_shifts')
def pickup_shifts():
    pass

#---------------------------------------------------------------------------
"""
shift_d = ShiftDetails(tutor_id = 2, shift_id = 4, status = 2)
        user.details.append(shift_d)
        db.session.add(user)
        db.session.commit()
"""
#---------------------------------------------------------------------------