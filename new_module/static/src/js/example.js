import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
publicWidget.registry.get_product = publicWidget.Widget.extend({
    selector:'.oe_structure',
    events:{
            'click.btn-add-cart':'_onClickSubmit',
    },
    start:function(){
    },
    _onClickSubmit : function(ev){
      console.log("lllllll",this)
    }



});