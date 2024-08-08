from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.restriction import role_required
from app.model import db, Shipping_data

user = Blueprint('user', __name__,
                 template_folder='../templates', static_folder='../static')


@user.route('/')
@login_required
@role_required('user')
def user_dashboard():
    all_data = Shipping_data.query.all()
    user_data = [data for data in all_data if data.user_id == current_user.id]
    other_data = [data for data in all_data if data.user_id != current_user.id]
    return render_template('user.html', user_data=user_data, other_data=other_data)


@user.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('user')
def add_shipping_data():
    if request.method == 'POST':
        try:
            new_data = Shipping_data(
                CS=request.form['CS'],
                week=int(request.form['week']),
                carrier=request.form['carrier'],
                service=request.form['service'],
                MV=request.form['MV'],
                SO=request.form['SO'],
                size=request.form['size'],
                POL=request.form['POL'],
                POD=request.form['POD'],
                Final_Destination=request.form['Final_Destination'],
                routing=request.form['routing'],
                CY_Open=datetime.strptime(request.form['CY_Open'], '%Y-%m-%d'),
                SI_Cut_Off=datetime.strptime(
                    request.form['SI_Cut_Off'], '%Y-%m-%d'),
                CY_CY_CLS=datetime.strptime(
                    request.form['CY_CY_CLS'], '%Y-%m-%d'),
                ETD=datetime.strptime(request.form['ETD'], '%Y-%m-%d'),
                ETA=datetime.strptime(request.form['ETA'], '%Y-%m-%d'),
                Contract_or_Coloader=request.form['Contract_or_Coloader'],
                shipper=request.form['shipper'],
                consignee=request.form['consignee'],
                term=request.form['term'],
                salesman=request.form['salesman'],
                cost=int(request.form['cost']),
                Rate_Valid=datetime.strptime(
                    request.form['Rate_Valid'], '%Y-%m-%d'),
                SR=request.form['SR'],
                HB_L=request.form['HB_L'],
                Remark=request.form['Remark'],
                user_id=current_user.id
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            # Handle the error and provide feedback to the user
            return f"An error occurred: {str(e)}"
        return redirect(url_for('user.user_dashboard'))
    return render_template('user_add_shipping_data.html')


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('user')
def edit_shipping_data(id):
    shipping_data = Shipping_data.query.get_or_404(id)
    if shipping_data.user_id != current_user.id:
        return redirect(url_for('user.user_dashboard'))

    if request.method == 'POST':
        try:
            shipping_data.CS = request.form['CS']
            shipping_data.week = int(request.form['week'])
            shipping_data.carrier = request.form['carrier']
            shipping_data.service = request.form['service']
            shipping_data.MV = request.form['MV']
            shipping_data.SO = request.form['SO']
            shipping_data.size = request.form['size']
            shipping_data.POL = request.form['POL']
            shipping_data.POD = request.form['POD']
            shipping_data.Final_Destination = request.form['Final_Destination']
            shipping_data.routing = request.form['routing']
            shipping_data.CY_Open = datetime.strptime(
                request.form['CY_Open'], '%Y-%m-%d')
            shipping_data.SI_Cut_Off = datetime.strptime(
                request.form['SI_Cut_Off'], '%Y-%m-%d')
            shipping_data.CY_CY_CLS = datetime.strptime(
                request.form['CY_CY_CLS'], '%Y-%m-%d')
            shipping_data.ETD = datetime.strptime(
                request.form['ETD'], '%Y-%m-%d')
            shipping_data.ETA = datetime.strptime(
                request.form['ETA'], '%Y-%m-%d')
            shipping_data.Contract_or_Coloader = request.form['Contract_or_Coloader']
            shipping_data.shipper = request.form['shipper']
            shipping_data.consignee = request.form['consignee']
            shipping_data.term = request.form['term']
            shipping_data.salesman = request.form['salesman']
            shipping_data.cost = int(request.form['cost'])
            shipping_data.Rate_Valid = datetime.strptime(
                request.form['Rate_Valid'], '%Y-%m-%d')
            shipping_data.SR = request.form['SR']
            shipping_data.HB_L = request.form['HB_L']
            shipping_data.Remark = request.form['Remark']
            db.session.commit()
        except ValueError as e:
            # Handle the error and provide feedback to the user
            return f"An error occurred: {str(e)}"
        return redirect(url_for('user.user_dashboard'))
    return render_template('user_edit_shipping_data.html', shipping_data=shipping_data)


@user.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required('user')
def delete_shipping_data(id):
    shipping_data = Shipping_data.query.get_or_404(id)
    if shipping_data.user_id != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('user.user_dashboard'))

    db.session.delete(shipping_data)
    db.session.commit()
    flash('Shipping data has been deleted.', 'success')
    return redirect(url_for('user.user_dashboard'))


@user.route('/search', methods=['GET', 'POST'])
@login_required
@role_required('user')
def search():
    # print("Search route")  # Debugging line
    q = request.args.get("q")
    if q:
        # print(f"Search query: {q}")  # Debugging line
        results = Shipping_data.query.filter(
            (Shipping_data.CS.ilike(f'%{q}%')) |
            (Shipping_data.week.ilike(f'%{q}%')) |
            (Shipping_data.carrier.ilike(f'%{q}%')) |
            (Shipping_data.service.ilike(f'%{q}%')) |
            (Shipping_data.MV.ilike(f'%{q}%')) |
            (Shipping_data.SO.ilike(f'%{q}%')) |
            (Shipping_data.size.ilike(f'%{q}%')) |
            (Shipping_data.POL.ilike(f'%{q}%')) |
            (Shipping_data.POD.ilike(f'%{q}%')) |
            (Shipping_data.Final_Destination.ilike(f'%{q}%')) |
            (Shipping_data.routing.ilike(f'%{q}%')) |
            (Shipping_data.CY_Open.ilike(f'%{q}%')) |
            (Shipping_data.SI_Cut_Off.ilike(f'%{q}%')) |
            (Shipping_data.CY_CY_CLS.ilike(f'%{q}%')) |
            (Shipping_data.ETD.ilike(f'%{q}%')) |
            (Shipping_data.ETA.ilike(f'%{q}%')) |
            (Shipping_data.Contract_or_Coloader.ilike(f'%{q}%')) |
            (Shipping_data.shipper.ilike(f'%{q}%')) |
            (Shipping_data.consignee.ilike(f'%{q}%')) |
            (Shipping_data.salesman.ilike(f'%{q}%')) |
            (Shipping_data.cost.ilike(f'%{q}%')) |
            (Shipping_data.Rate_Valid.ilike(f'%{q}%')) |
            (Shipping_data.SR.ilike(f'%{q}%')) |
            (Shipping_data.HB_L.ilike(f'%{q}%'))
        ).order_by(Shipping_data.carrier.asc(), Shipping_data.service.desc()).limit(100).all()
        # print(f"Results count: {len(results)}")  # Debugging line
    else:
        results = []

    return render_template("user_search_results.html", results=results)
