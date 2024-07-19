from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.restriction import role_required
from app.model import db, Shipping_data

user = Blueprint('user', __name__,
                 template_folder='../templates', static_folder='../static')


@user.route('/')
@login_required
@role_required('user')
def user_dashboard():
    # Getting the current user id for later use
    user_data = Shipping_data.query.filter_by(user_id=current_user.id).all()
    return render_template('user.html', user_data=user_data)


@user.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('user')
def add_shipping_data():
    if request.method == 'POST':
        new_data = Shipping_data(
            CS=request.form['CS'],
            week=request.form['week'],
            carrier=request.form['carrier'],
            service=request.form['service'],
            MV=request.form['MV'],
            SO=request.form['SO'],
            size=request.form['size'],
            POL=request.form['POL'],
            POD=request.form['POD'],
            Final_Destination=request.form['Final_Destination'],
            routing=request.form['routing'],
            CY_Open=request.form['CY_Open'],
            SI_Cut_Off=request.form['SI_Cut_Off'],
            CY_CV_CLS=request.form['CY_CV_CLS'],
            ETD=request.form['ETD'],
            ETA=request.form['ETA'],
            Contract_or_Coloader=request.form['Contract_or_Coloader'],
            shipper=request.form['shipper'],
            consignee=request.form['consignee'],
            term=request.form['term'],
            salesman=request.form['salesman'],
            cost=request.form['cost'],
            ATE_Valid=request.form['ATE_Valid'],
            SR=request.form['SR'],
            HB_L=request.form['HB_L'],
            Remark=request.form['Remark'],
            user_id=current_user.id
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('user.user_dashboard'))
    return render_template('add_shipping_data.html')


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('user')
def edit_shipping_data(id):
    shipping_data = Shipping_data.query.get_or_404(id)
    if shipping_data.user_id != current_user.id:
        return redirect(url_for('user.user_dashboard'))

    if request.method == 'POST':
        shipping_data.CS = request.form['CS']
        shipping_data.week = request.form['week']
        shipping_data.carrier = request.form['carrier']
        shipping_data.service = request.form['service']
        shipping_data.MV = request.form['MV']
        shipping_data.SO = request.form['SO']
        shipping_data.size = request.form['size']
        shipping_data.POL = request.form['POL']
        shipping_data.POD = request.form['POD']
        shipping_data.Final_Destination = request.form['Final_Destination']
        shipping_data.routing = request.form['routing']
        shipping_data.CY_Open = request.form['CY_Open']
        shipping_data.SI_Cut_Off = request.form['SI_Cut_Off']
        shipping_data.CY_CV_CLS = request.form['CY_CV_CLS']
        shipping_data.ETD = request.form['ETD']
        shipping_data.ETA = request.form['ETA']
        shipping_data.Contract_or_Coloader = request.form['Contract_or_Coloader']
        shipping_data.shipper = request.form['shipper']
        shipping_data.consignee = request.form['consignee']
        shipping_data.term = request.form['term']
        shipping_data.salesman = request.form['salesman']
        shipping_data.cost = request.form['cost']
        shipping_data.ATE_Valid = request.form['ATE_Valid']
        shipping_data.SR = request.form['SR']
        shipping_data.HB_L = request.form['HB_L']
        shipping_data.Remark = request.form['Remark']
        db.session.commit()
        return redirect(url_for('user.user_dashboard'))
    return render_template('edit_shipping_data.html', shipping_data=shipping_data)
