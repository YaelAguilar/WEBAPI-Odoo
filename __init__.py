from flask import Flask, jsonify, request
import xmlrpc.client
import pyodbc
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return """ 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WEBAPI Odoo</title>
        </head>
        <body style="background-color:#e4e2e5;min-height:100%;min-width:80vh;padding-left:5%;padding-right:5%;padding-top:3%">
            <div style="height:30%">
                <span style="color:red">WEB API Odoo</span>
                <a href="https://www.odoo.com/documentation/17.0/es/developer/reference/external_api.html">Documentacion</a>
                <a href="#" onclick="mostrarDiagrama()">Diagrama</a>
            </div>
            <div style="height:30%">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <a onclick="esperar('Información de clientes', 'Cargando la consulta', 4500)" href="./prueba" target="iframeView" class="btn btn-primary" style="width:10%;border: thick black;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-inbox" viewBox="0 0 16 16">
                    <path d="M4.98 4a.5.5 0 0 0-.39.188L1.54 8H6a.5.5 0 0 1 .5.5 1.5 1.5 0 1 0 3 0A.5.5 0 0 1 10 8h4.46l-3.05-3.812A.5.5 0 0 0 11.02 4H4.98zm9.954 5H10.45a2.5.5 0 0 1-4.9 0H1.066l.32 2.562a.5.5 0 0 0 .497.438h12.234a.5.5 0 0 0 .496-.438L14.933 9zM3.809 3.563A1.5 1.5 0 0 1 4.981 3h6.038a1.5 1.5 0 0 1 1.172.563l3.7 4.625a.5.5 0 0 1 .105.374l-.39 3.124A1.5 1.5 0 0 1 14.117 13H1.883a1.5 1.5 0 0 1-1.489-1.314l-.39-3.124a.5.5 0 0 1 .106-.374l3.7-4.625z"/>
                    </svg> Ver datos clientes</a>
                    
                    <a onclick="esperar('Facturas de clientes', 'Cargando la consulta', 4500)" href="./facturas" target="iframeView" class="btn btn-secondary" style="width:10%;border: thick black;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-text" viewBox="0 0 16 16">
                    <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h4.5L14 4.5zM8 1v3h3.5L8 1zM5 9a.5.5 0 0 1 .5-.5H8a.5.5 0 0 1 0 1H5.5a.5.5 0 0 1-.5-.5zM5 11.5a.5.5 0 0 1 .5-.5H8a.5.5 0 0 1 0 1H5.5a.5.5 0 0 1-.5-.5zM5 14a.5.5 0 0 1 .5-.5H8a.5.5 0 0 1 0 1H5.5a.5.5 0 0 1-.5-.5z"/>
                    </svg> Facturas de cliente</a>

                    <a onclick="esperar('Apuntes contables clientes', 'Cargando la consulta', 4500)" href="./apuntes_contables" target="iframeView" class="btn btn-success" style="width:15%;border: thick black;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-journal-bookmark" viewBox="0 0 16 16">
                    <path d="M6 8V1h1v7l2-2 2 2V1h1v7.5l-2-2-2 2-2-2z"/>
                    <path d="M4.5 0A1.5 1.5 0 0 0 3 1.5v13A1.5 1.5 0 0 0 4.5 16h7a1.5 1.5 0 0 0 1.5-1.5v-13A1.5 1.5 0 0 0 11.5 0h-7zm0 1h7A.5.5 0 0 1 12 1.5V4H4V1.5A.5.5 0 0 1 4.5 1z"/>
                    </svg> Apuntes contables clientes</a>
                </div>
            </div>
            <div style="border-style: solid;border-color: black;width:100%;height:80vh">
                <iframe width="100%" height="100%" id="iframeView" name="iframeView" src=""></iframe>
            </div>
        </body>
        <script>
            function esperar(titulo, mensaje, tiempo){
                let timerInterval;
                Swal.fire({
                title: titulo,
                html: mensaje,
                timer: tiempo,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                    const timer = Swal.getPopup().querySelector("b");
                    timerInterval = setInterval(() => {
                    
                    }, 100);
                },
                willClose: () => {
                    clearInterval(timerInterval);
                }
                }).then((result) => {
                    if (result.dismiss === Swal.DismissReason.timer) {
                    }
                });
            }
            function mostrarDiagrama(){
                Swal.fire({
                    html: `<iframe src="https://drive.google.com/file/d/1eVcEwVqS-QoPAeIMoj07HLNk_vuo3OnD/preview" width="640" height="480" allow="autoplay"></iframe>`,
                    width: 900
                });
            }
        </script>
        </html>
    """

@app.route("/prueba/", methods=["POST", "GET"])
def oddo():
    url = "https://edu-atipruebas.odoo.com/"
    db = "edu-estancia"
    username = "atiasesores.tester3@gmail.com"
    password = "A7QiM!L_5Ls-dje"

    common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
    versión = common.version()
    print("detalles...", versión)
    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
    ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['id', '>', '0']]], {'limit': 100})

    registrospantalla = """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <table class="table table-dark" style="margin=5%">
        <tr><th>Nombre</th><th>website</th><th>comment</th><th>Email</th><th>Compañia</th><th>Teléfono</th><th>Móvil</th><th>Identificación Fiscal</th><th>ID Contacto</th><th>Puesto de Trabajo</th><th>Etiquetas</th><th>Número de Cuenta</th><th>CLABE</th><th>Banco</th><th>Enviar Dinero</th><th>Formato</th><th>Cuenta por Cobrar</th><th>Cuenta por Pagar</th><th>Nacionalidad</th><th>Tipo de Operación</th><th>Registro</th></tr>"""

    for x in ids:
        registro = models.execute_kw(db, uid, password, 'res.partner', 'read', [x], {
            'fields': [
                'name', 'website', 'comment', 'email', 'is_company',
                'phone', 'mobile', 'vat', 'x_studio_idcontacto', 'function', 'category_id',
                'ubl_cii_format', 'property_account_receivable_id', 'property_account_payable_id', 'l10n_mx_nationality', 'l10n_mx_type_of_operation'
            ]
        })
        
        name = registro[0].get('name', '')
        website = registro[0].get('website', '')
        comment = registro[0].get('comment', '')
        email = registro[0].get('email', '')
        is_company = registro[0].get('is_company', '')
        phone = registro[0].get('phone', '')
        mobile = registro[0].get('mobile', '')
        vat = registro[0].get('vat', '')
        idcontacto = registro[0].get('x_studio_idcontacto', '')
        function = registro[0].get('function', '')
        category_id = str(registro[0].get('category_id', ''))
        ubl_cii_format = registro[0].get('ubl_cii_format', '')
        property_account_receivable_id = str(registro[0].get('property_account_receivable_id', ''))
        property_account_payable_id = str(registro[0].get('property_account_payable_id', ''))
        l10n_mx_nationality = registro[0].get('l10n_mx_nationality', '')
        l10n_mx_type_of_operation = registro[0].get('l10n_mx_type_of_operation', '')
        
        banks = models.execute_kw(db, uid, password, 'res.partner.bank', 'search_read', [[['partner_id', '=', x]]], {
            'fields': ['acc_number', 'l10n_mx_edi_clabe', 'bank_id', 'allow_out_payment'],
            'limit': 1
        })
        acc_number = banks[0].get('acc_number', '') if banks else ''
        l10n_mx_edi_clabe = banks[0].get('l10n_mx_edi_clabe', '') if banks else ''
        bank_id = str(banks[0].get('bank_id', '')) if banks else ''
        allow_out_payment = 1 if banks and banks[0].get('allow_out_payment', False) else 0

        registrospantalla += f"<tr><td>{name}</td><td>{website}</td><td>{comment}</td><td>{email}</td><td>{is_company}</td><td>{phone}</td><td>{mobile}</td><td>{vat}</td><td>{idcontacto}</td><td>{function}</td><td>{category_id}</td><td>{acc_number}</td><td>{l10n_mx_edi_clabe}</td><td>{bank_id}</td><td>{allow_out_payment}</td><td>{ubl_cii_format}</td><td>{property_account_receivable_id}</td><td>{property_account_payable_id}</td><td>{l10n_mx_nationality}</td><td>{l10n_mx_type_of_operation}</td><td>{str(x)}</td></tr>"

        insertarPartner(name, website, comment, email, is_company, phone, mobile, vat, idcontacto, function, category_id, acc_number, l10n_mx_edi_clabe, bank_id, allow_out_payment, ubl_cii_format, property_account_receivable_id, property_account_payable_id, l10n_mx_nationality, l10n_mx_type_of_operation)

    return registrospantalla

@app.route("/facturas/", methods=["POST", "GET"])
def facturas():
    url = "https://edu-atipruebas.odoo.com/"
    db = "edu-estancia"
    username = "atiasesores.tester3@gmail.com"
    password = "A7QiM!L_5Ls-dje"

    common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    ids = models.execute_kw(db, uid, password, 'account.move', 'search', [[['move_type', '=', 'out_invoice']]], {'limit': 100})

    registrospantalla = """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <table class="table table-dark" style="margin=5%">
        <tr><th>Cliente</th><th>Forma de pago</th><th>Política de pago</th><th>Uso</th><th>CFDI al público</th><th>Fecha de factura</th><th>Fecha de vencimiento</th><th>Referencia de pago</th><th>Términos de pago</th><th>Diario</th><th>Origen del CFDI</th></tr>"""

    for x in ids:
        registro = models.execute_kw(db, uid, password, 'account.move', 'read', [x], {
            'fields': [
                'partner_id', 'l10n_mx_edi_payment_method_id', 'l10n_mx_edi_payment_policy', 'l10n_mx_edi_usage',
                'l10n_mx_edi_cfdi_to_public', 'invoice_date', 'invoice_date_due', 'payment_reference', 'invoice_payment_term_id',
                'journal_id', 'l10n_mx_edi_cfdi_origin'
            ]
        })
        
        partner_id = registro[0].get('partner_id', [])[1] if registro[0].get('partner_id') else ''
        l10n_mx_edi_payment_method_id = registro[0].get('l10n_mx_edi_payment_method_id', [])[1] if registro[0].get('l10n_mx_edi_payment_method_id') else ''
        l10n_mx_edi_payment_policy = registro[0].get('l10n_mx_edi_payment_policy', '')
        l10n_mx_edi_usage = registro[0].get('l10n_mx_edi_usage', '')
        l10n_mx_edi_cfdi_to_public = registro[0].get('l10n_mx_edi_cfdi_to_public', False)
        invoice_date = registro[0].get('invoice_date', '')
        invoice_date_due = registro[0].get('invoice_date_due', '')
        payment_reference = registro[0].get('payment_reference', '')
        invoice_payment_term_id = registro[0].get('invoice_payment_term_id', [])[1] if registro[0].get('invoice_payment_term_id') else ''
        journal_id = registro[0].get('journal_id', [])[1] if registro[0].get('journal_id') else ''
        l10n_mx_edi_cfdi_origin = registro[0].get('l10n_mx_edi_cfdi_origin', '')

        registrospantalla += f"<tr><td>{partner_id}</td><td>{l10n_mx_edi_payment_method_id}</td><td>{l10n_mx_edi_payment_policy}</td><td>{l10n_mx_edi_usage}</td><td>{l10n_mx_edi_cfdi_to_public}</td><td>{invoice_date}</td><td>{invoice_date_due}</td><td>{payment_reference}</td><td>{invoice_payment_term_id}</td><td>{journal_id}</td><td>{l10n_mx_edi_cfdi_origin}</td></tr>"

        insertarFactura(partner_id, l10n_mx_edi_payment_method_id, l10n_mx_edi_payment_policy, l10n_mx_edi_usage, l10n_mx_edi_cfdi_to_public, invoice_date, invoice_date_due, payment_reference, invoice_payment_term_id, journal_id, l10n_mx_edi_cfdi_origin)

    return registrospantalla

@app.route("/apuntes_contables/", methods=["POST", "GET"])
def apuntes_contables():
    url = "https://edu-atipruebas.odoo.com/"
    db = "edu-estancia"
    username = "atiasesores.tester3@gmail.com"
    password = "A7QiM!L_5Ls-dje"

    common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    ids = models.execute_kw(db, uid, password, 'account.move.line', 'search', [[['id', '>', '0']]], {'limit': 100})

    registrospantalla = """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <table class="table table-dark" style="margin=5%">
        <tr><th>Cuenta</th><th>Etiqueta</th><th>Débito</th><th>Crédito</th><th>Tablas de impuestos</th></tr>"""

    for x in ids:
        registro = models.execute_kw(db, uid, password, 'account.move.line', 'read', [x], {
            'fields': [
                'account_id', 'name', 'debit', 'credit', 'tax_tag_ids'
            ]
        })
        
        account_id = registro[0].get('account_id', [])[1] if registro[0].get('account_id') else ''
        name = registro[0].get('name', '')
        debit = registro[0].get('debit', 0.0)
        credit = registro[0].get('credit', 0.0)
        
        tax_tag_ids = ", ".join(str(tag) for tag in registro[0].get('tax_tag_ids', [])) if registro[0].get('tax_tag_ids') else ''

        registrospantalla += f"<tr><td>{account_id}</td><td>{name}</td><td>{debit}</td><td>{credit}</td><td>{tax_tag_ids}</td></tr>"

        insertarApunteContable(account_id, name, debit, credit, tax_tag_ids)

    return registrospantalla

def insertarPartner(name, website, comment, email, is_company, phone, mobile, vat, idcontacto, function, category_id, acc_number, l10n_mx_edi_clabe, bank_id, allow_out_payment, ubl_cii_format, property_account_receivable_id, property_account_payable_id, l10n_mx_nationality, l10n_mx_type_of_operation):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=estancia-1.cwh2wgvynejc.us-east-1.rds.amazonaws.com;DATABASE=adOddo;UID=admin;PWD=quemasquieres')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM partner WHERE name = ?", (name,))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO partner (name, website, comment, email, is_company, phone, mobile, vat, idcontacto, [function], category_id, acc_number, l10n_mx_edi_clabe, bank_id, allow_out_payment, ubl_cii_format, property_account_receivable_id, property_account_payable_id, l10n_mx_nationality, l10n_mx_type_of_operation) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (
                name, website, comment, email, is_company, phone, mobile, vat, idcontacto, function, category_id,
                acc_number, l10n_mx_edi_clabe, bank_id, allow_out_payment, ubl_cii_format,
                property_account_receivable_id, property_account_payable_id, l10n_mx_nationality,
                l10n_mx_type_of_operation
            )
        )

        conn.commit()

    cursor.close()
    conn.close()

def insertarFactura(partner_id, l10n_mx_edi_payment_method_id, l10n_mx_edi_payment_policy, l10n_mx_edi_usage, l10n_mx_edi_cfdi_to_public, invoice_date, invoice_date_due, payment_reference, invoice_payment_term_id, journal_id, l10n_mx_edi_cfdi_origin):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=estancia-1.cwh2wgvynejc.us-east-1.rds.amazonaws.com;DATABASE=adOddo;UID=admin;PWD=quemasquieres')
    cursor = conn.cursor()

    try:
        payment_term_date = datetime.strptime(invoice_payment_term_id, '%Y-%m-%d').date()
        invoice_payment_term_id_sql = payment_term_date
    except ValueError:
        invoice_payment_term_id_sql = invoice_payment_term_id

    cursor.execute("SELECT id FROM factura WHERE partner_id = ? AND invoice_date = ?", (partner_id, invoice_date))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO factura (partner_id, l10n_mx_edi_payment_method_id, l10n_mx_edi_payment_policy, l10n_mx_edi_usage, l10n_mx_edi_cfdi_to_public, invoice_date, invoice_date_due, payment_reference, invoice_payment_term_id, journal_id, l10n_mx_edi_cfdi_origin) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (
                partner_id, l10n_mx_edi_payment_method_id, l10n_mx_edi_payment_policy, l10n_mx_edi_usage,
                l10n_mx_edi_cfdi_to_public, invoice_date, invoice_date_due, payment_reference,
                invoice_payment_term_id_sql,
                journal_id, l10n_mx_edi_cfdi_origin
            )
        )

        conn.commit()

    cursor.close()
    conn.close()

def insertarApunteContable(account_id, name, debit, credit, tax_tag_ids):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=estancia-1.cwh2wgvynejc.us-east-1.rds.amazonaws.com;DATABASE=adOddo;UID=admin;PWD=quemasquieres')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM apunte_contable WHERE account_id = ? AND name = ?", (account_id, name))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO apunte_contable (account_id, name, debit, credit, tax_tag_ids) 
            VALUES (?, ?, ?, ?, ?)
            """, 
            (
                account_id, name, debit, credit, tax_tag_ids
            )
        )

        conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    host="0.0.0.0"
    port=3002
    app.run(host=host, port=port, debug=True)
