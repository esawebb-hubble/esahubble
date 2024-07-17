/*
# esahubble.org
# Copyright 2009-2010 ESO, ESA/Hubble, IAU
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
*/

/* 
 * External link decorator 
 */
(function($) {
    $.fn.extend({
        extlink: function () {
            $("a", this).filter(function (i) {
                return (($(this).attr("target") == '_blank') && $(this).contents('img').size()==0);
            }).each(function () {
                $(this).addClass("extlink")
            });
        }
    });
})(jQuery);


$(document).ready(function () {
    $(this).extlink();
});


/* onFocus/onBlur events for search fields */
function searchbox_focus( box, text ) {
	if( box.value == text ){
		box.value='';
		box.className = box.className + '_ready';
	}
}

function searchbox_blur( box, text ) {
	if( box.value == '' ){
		box.value=text;
		box.className = box.className.split('_ready',1)[0];
	}
}


        
/* feature rotator */

$(".rotator").hover(
          function () {
              $(".fbut").fadeIn();
              
          }, 
          function () {
             $(".fbut").fadeOut();
          }
        )
        
$('.feature-fade').removeClass("init_hide")

$('.rotator .items' ).
            cycle({ 
                fx:    'fade', 
                timeout: 4000,
                speed:  1000,
                pause:  1,
                next:   '.fbut_right', 
                prev:   '.fbut_left',
                pager: '#feat-nav'
            });;

$('.fbut').fadeOut(0);
$('.fbut').removeClass('init_hide');


/* Advanced search form submission. removes unset parameters
 * */
$(document).ready( function(){
    function process_adv_search_parms() {
        var fields = $("#adv_search_data :input").serializeArray();
        var goodfields = []
		jQuery.each(fields, function(i, field){
        	
        	
        	if (field.value != '0' && field.value != null && field.value != '')
        	{
        		goodfields.push(field)
        		
        	}
        });
    	goodfields.push({name:'adv',value:''})
    	//return goodfields
        return $.param(goodfields)
      }

      // $(":checkbox, :radio").click(showValues);
      $("#adv_search_data").submit(function() {
    	  
    	  params = process_adv_search_parms()
    	  window.location = "?" + params
    	  
    	  return false
    });
      
});


/* static files tracking */
$('a[href*="'+MEDIA_URL+'"]').addClass('ga_static_tracking')
$('.ga_static_tracking').click(function() { 
	pageTracker._trackPageview($(this).attr('href'))
})
