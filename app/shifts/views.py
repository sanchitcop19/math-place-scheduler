from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.models import Shift, ShiftDetails, User
from app.shifts.forms import DropForm, PickupForm, AddForm
import sys, time
from math import floor, isclose
from app.shifts.store import Shift_Enum, num_tutors

shifts = Blueprint('shifts', __name__)


def translate_time(shift):
    if not shift:
        return None
    shift_start = shift[0]
    shift_start = time.strptime(shift_start, "%H:%M")
    shift_end = shift[1]
    shift_end = time.strptime(shift_end, "%H:%M")
    return (shift_start.tm_hour + (0.5 if shift_start.tm_min == 30 else 0.0), shift_end.tm_hour + (0.5 if shift_end.tm_min == 30 else 0.0))


@shifts.route('/add_shifts')
@login_required
def add_shifts():
    return redirect(url_for('main.index'))
    '''
    user = current_user
    shifts = Shift.query.all()
    store = []
    shifts_s = []
    shifts_f = []

    for shift in shifts:
        if not isclose(floor(shift.start),shift.start, abs_tol=0.00001):
            shift_f = str(shift.end) + ":00"
            shift = (str(floor(shift.start))+ ":30")

        else:
            shift_f = str(floor(shift.end)) + ":30"
            shift = str(shift.start) + ":00"

        shifts_s.append(shift)
        shifts_f.append(shift_f)
        store = zip(shifts_s, shifts_f)
    
    store = list(map(translate_time, store))

    if form.validate_on_submit():
        user = current_user
        if user is not None:
            # figure out which shifts to drop
            for item in store:
                print(item)
            for item in store:
                if request.form.get(''.join(("slot_", str(item[0])))):
                    shift = Shift.query.filter_by(start = item[0]).first().id
                    save = ShiftDetails.query.filter_by(tutor_id = user.id, shift_id = shift).first()
                    save.status = 1
                    db.session.commit()
            #TODO: add validation for legal shift
        return redirect(url_for('shifts.drop_shifts'))

    return render_template('shifts/add_shifts.html', **locals()) 
'''

@login_required
@shifts.route('/drop_shifts', methods = ['GET', 'POST'])
def drop_shifts():

    user = current_user
    store = [[]]*4
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    form = DropForm()

    for i, day in enumerate(days, start = 1):
        shift_details = ShiftDetails.query.filter_by(tutor_id = current_user.id, day = i).all()
        for detail in shift_details:
            shifts_s = []
            shifts_f = []
            if detail and detail.status == Shift_Enum.ASSIGNED.value or (detail.status == Shift_Enum.PICKED_UP.value and detail.coverer == user.id):
                shift = Shift.query.filter_by(id = detail.shift_id).first()
                if not isclose(floor(shift.start),shift.start, abs_tol=0.00001):
                    shift_f = str(shift.end) + ":00"
                    shift = (str(floor(shift.start))+ ":30")

                else:
                    shift_f = str(floor(shift.end)) + ":30"
                    shift = str(shift.start) + ":00"

                shifts_s.append(shift)
                shifts_f.append(shift_f)
                if not store[i-1]:
                    store[i-1] = [(zip(shifts_s, shifts_f))]
                else:
                    store[i-1].append((zip(shifts_s, shifts_f)))

        shift_details = ShiftDetails.query.filter_by(coverer=current_user.id, day=i).all()
        print(shift_details)
        for detail in shift_details:

            shifts_s = []
            shifts_f = []
            if detail and detail.status == Shift_Enum.PICKED_UP.value and detail.tutor_id != user.id:
                shift = Shift.query.filter_by(id = detail.shift_id).first()

                if not isclose(floor(shift.start),shift.start, abs_tol=0.00001):
                    shift_f = str(shift.end) + ":00"
                    shift = (str(floor(shift.start))+ ":30")

                else:
                    shift_f = str(floor(shift.end)) + ":30"
                    shift = str(shift.start) + ":00"

                shifts_s.append(shift)
                shifts_f.append(shift_f)

                store[i-1].append(zip(shifts_s, shifts_f))

    #print([translate_time(item) for item in store])
    for i, day in enumerate(store):
        if not day:
            continue
        for j, item in enumerate(day):
            store[i][j] = list(map(translate_time, item))

    if form.validate_on_submit():
        user = current_user
        if user is not None:
            # figure out which shifts to drop
            for i, day in enumerate(days, start = 1):
                if store[i-1]:
                    for item in store[i-1]:
                        for time in item:
                            if request.form.get(''.join(("slot_", str(time[0])))):
                                shift = Shift.query.filter_by(start = time[0]).first().id
                                save = ShiftDetails.query.filter_by(tutor_id = user.id, shift_id = shift, day = i).first()
                                if not save:
                                    save = ShiftDetails.query.filter_by(coverer = user.id, shift_id = shift, day = i).first()
                                save.status = 1
                                db.session.commit()
                        #TODO: add validation for legal shift
        return redirect(url_for('shifts.drop_shifts'))

    return render_template('shifts/drop_shifts.html', **locals())

@login_required
@shifts.route('/pickup_shifts', methods = ['GET', 'POST'])
def pickup_shifts():

    user = current_user
    store = [None]*4
    tutor_ids = [i for i in range(2, num_tutors + 2)]
    tutors = ["Sanchit", "Jane", "Emily", "Cece", "Michael", "Jake", "Matthew", "Milos", "Mitchell", "Nicholas", "Quan", "Razul", "Shoujing", "Hannah"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    form = PickupForm()

    for i, day in enumerate(days, start = 1):
        shift_details = ShiftDetails.query.filter_by(status = 1, day = i).all()

        for detail in shift_details:
            shifts_s = []
            shifts_f = []
            shift = Shift.query.filter_by(id = detail.shift_id).first()

            if not isclose(floor(shift.start),shift.start, abs_tol=0.00001):
                shift_f = str(shift.end) + ":00"
                shift = (str(floor(shift.start))+ ":30")

            else:
                shift_f = str(floor(shift.end)) + ":30"
                shift = str(shift.start) + ":00"

            shifts_s.append(shift)
            shifts_f.append(shift_f)

 
            if not store[i-1]:
                store[i-1] = [(tuple(zip(shifts_s, shifts_f)), detail.tutor_id)]
            else:
                store[i-1].append((tuple(zip(shifts_s, shifts_f)), detail.tutor_id))

    for i, day in enumerate(days, start = 1):
        if not store[i-1]:
            continue
        for j, shift in enumerate(store[i-1]):
            store[i-1][j] = (list(map(translate_time, store[i-1][j][0])), store[i-1][j][1])
    for item in store:
        print(item, "\n")
    if form.validate_on_submit():
        user = current_user
        if user is not None:
            for i, day in enumerate(days, start = 1):
                if store[i-1]:
                    for item in store[i-1]:
                        start = item[0][0][0]
                        tut_id = item[1]

                        if request.form.get(''.join(("slot_", str(start), "_", str(tut_id)))):
                            shift = Shift.query.filter_by(start = start).first().id
                            save = ShiftDetails.query.filter_by(tutor_id = tut_id, shift_id = shift, day = i).first()
                            save.status = 2
                            save.coverer = user.id
                            db.session.commit()
                    #TODO: add validation for legal shift
        return redirect(url_for('shifts.pickup_shifts'))

    return render_template('shifts/pickup_shifts.html', **locals())
 
#-------------------------------------------------------------------------
"""
shift_d = ShiftDetails(tutor_id = 2, shift_id = 4, status = 2)
        user.details.append(shift_d)
        db.session.add(user)
        db.session.commit()
"""
#---------------------------------------------------------------------------
