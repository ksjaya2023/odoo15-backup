## Update from Odoo Studio notes

- 20/09/23 Update 'Approve Reservation and Create issue when inprogess' server action.

Add this part on create stock.move > 'analytic_account_id': line.x_studio_analytic_account.id or False.

Change the destination location.

opr_type = env['stock.picking.type'].search([('name','=','Inventory Issued'), ('warehouse_id', '=', line.x_studio_warehouse.id)], limit=1)

rec_gi = env['stock.picking'].create({'location_dest_id': opr_type.default_location_dest_id.id,
                                                     'location_id':rec_src_loc,
                                                     'picking_type_id':rec_opr_type,
                                                     'x_studio_many2one_reservation':line.id,
                                                     'x_studio_create_by_reservation':1,
          })

for item in line.x_reservation_line_ids_f5c60:
              env['stock.move'].create({'product_id':item.x_studio_many2one_field_vym0h.id, 
                                        'product_uom_qty':item.x_studio_quantity,
                                        'picking_id':gi_id,
                                        'name':item.x_studio_many2one_field_vym0h.name,
                                        'product_uom':item.x_studio_uom.id,
                                        'location_id':rec_src_loc,
                                        'location_dest_id': opr_type.default_location_dest_id.id,
                                        'analytic_account_id': line.x_studio_analytic_account.id or False,
              })


- 21/09/23 Update 'Odoo Studio: stock.picking.form customization' view.

Remove analytic account from view.
  <xpath expr="//form[1]/sheet[1]/group[1]/group[2]/field[@name='origin']" position="after">
    <field name="purchase_id"/>
    <field name="x_studio_analytic_account" string="Analytic Account" attrs="{&quot;readonly&quot;: [[&quot;x_studio_is_editable&quot;,&quot;=&quot;,False]]}"/> (This part)
    <field name="x_studio_return_request" attrs="{&quot;invisible&quot;: [[&quot;x_studio_return_request&quot;,&quot;=&quot;,False]]}"/>
    <field name="x_studio_created_pr_on_po" string="Created PR on PO"/>
    <field name="create_uid"/>
    <field name="x_studio_create_pr" string="Create PR" attrs="{}" invisible="1"/>
    <field name="x_studio_create_by_reservation" string="Create by Reservation" attrs="{}" invisible="1"/>
  </xpath>

- 21/09/23 Comment this automation on 'Angga Add approval to account.move'.

  <!-- # ambil nomor GI dari reference utk get analytic account by said
  # if record.ref:
  #   find1 = record.ref.find('/')
  #   if find1 > 0:
  #     gi_var = record.ref.split('/')
  #     if gi_var[1] == 'OUT' or gi_var[1] == 'RET': 
  #       find2 = record.ref.find(' ')
  #       if find2 > 0:
  #         gi_text = record.ref.split(' ')
  #         gi_name = gi_text[0]
          
  #         if gi_name:
  #           analytic_acc_id = 0
  #           gi = env['stock.picking'].search([('name','=',gi_name)])
  #           for line_gi in gi:
  #             analytic_acc_id = line_gi.x_studio_analytic_account.id
            
  #           # if analytic_acc_id:
  #           for item_jurnal in record.line_ids:
  #             if item_jurnal.credit:
  #               item_jurnal['analytic_account_id'] = analytic_acc_id -->

- 22/09/23 Update 'Odoo Studio: purchase.request.form customization' view.

- 23/09/23 Update 'Odoo Studio: stock.picking.form customization' view.

Comment:
  <xpath expr="//form[1]/sheet[1]/notebook[1]/page[@name='operations']/field[@name='move_ids_without_package']/tree[1]/field[@name='quantity_done']" position="attributes">-->
   <attribute name="attrs">{"readonly": [["is_quantity_done_editable","=",False]], "column_invisible": [["parent.state","=","draft"],["parent.immediate_transfer","=",False]]}</attribute>
   <attribute name="invisible">1</attribute>
  </xpath>


  

