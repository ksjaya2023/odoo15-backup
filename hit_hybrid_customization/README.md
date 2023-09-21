## Update from Odoo Studio notes

- 20/Update 'Approve Reservation and Create issue when inprogess' server action.

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


- Update 'Odoo Studio: stock.picking.form customization' view.

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