odoo.define('direct_print.pos_save_receipt', function (require) {
    'use strict';

    const Order = require('point_of_sale.Order');
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosSaveReceiptOrder = (Order) => class PosSaveReceiptOrder extends Order {
        export_for_printing() {
            const result = super.export_for_printing(...arguments);
            
            // The POS ticket is rendered using QWeb.
            // We can get the rendered receipt and send it to the backend.
            const receipt_html = this.pos.env.qweb.render('OrderReceipt', {
                receipt: this.export_for_printing(),
                order: this,
                widget: this.pos.chrome,
                pos: this.pos,
                moment: moment,
            });

            if (receipt_html) {
                rpc.query({
                    model: 'pos.receipt',
                    method: 'create_from_pos',
                    args: [receipt_html],
                    kwargs: {
                        context: this.pos.session.user_context,
                    },
                }).then(function (result) {
                    // Receipt saved successfully
                    console.log('POS receipt saved:', result);
                }).catch(function (error) {
                    console.error('Could not save POS receipt:', error);
                });
            }

            return result;
        }
    };

    Registries.Model.extend(Order, PosSaveReceiptOrder);
});
