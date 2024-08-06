from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ..restriction import role_required
from ..model import db, Shipping_data

admin = Blueprint('admin', __name__,
                 template_folder='../../templates', static_folder='../../static')


@admin.route('/')
@login_required
@role_required('admin')
def admin_dashboard():
    user_data = Shipping_data.query.all()  # Admin can see all shipping data
    return render_template('admin.html', user_data=user_data)


@admin.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
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
            CY_CY_CLS=request.form['CY_CY_CLS'],
            ETD=request.form['ETD'],
            ETA=request.form['ETA'],
            Contract_or_Coloader=request.form['Contract_or_Coloader'],
            shipper=request.form['shipper'],
            consignee=request.form['consignee'],
            term=request.form['term'],
            salesman=request.form['salesman'],
            cost=request.form['cost'],
            Rate_Valid=request.form['Rate_Valid'],
            SR=request.form['SR'],
            HB_L=request.form['HB_L'],
            Remark=request.form['Remark'],
            user_id=current_user.id
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('add_shipping_data.html')


@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_shipping_data(id):
    shipping_data = Shipping_data.query.get_or_404(id)

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
        shipping_data.CY_CY_CLS = request.form['CY_CY_CLS']
        shipping_data.ETD = request.form['ETD']
        shipping_data.ETA = request.form['ETA']
        shipping_data.Contract_or_Coloader = request.form['Contract_or_Coloader']
        shipping_data.shipper = request.form['shipper']
        shipping_data.consignee = request.form['consignee']
        shipping_data.term = request.form['term']
        shipping_data.salesman = request.form['salesman']
        shipping_data.cost = request.form['cost']
        shipping_data.Rate_Valid = request.form['Rate_Valid']
        shipping_data.SR = request.form['SR']
        shipping_data.HB_L = request.form['HB_L']
        shipping_data.Remark = request.form['Remark']
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('edit_shipping_data.html', shipping_data=shipping_data)

@admin.route('/search', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def search():
    #print("Search route")  # Debugging line
    q = request.args.get("q")
    if q:
        #print(f"Search query: {q}")  # Debugging line
        results = Shipping_data.query.filter(
            (Shipping_data.id.ilike(f'%{q}%')) |
            (Shipping_data.date_created.ilike(f'%{q}%')) |
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
        #print(f"Results count: {len(results)}")  # Debugging line
    else:
        results = []
    
    return render_template("admin_search_results.html", results=results)