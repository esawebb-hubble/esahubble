// Mobile menu

$(document).ready(function() {
	$('.menu-trigger').click(function(){
		$('.level0').toggleClass('open-menu');
		return false;
	});

	$('.mobile-children').click(function(event){
		$(this).parent().find('ul:first').toggleClass('open-menu');
		return false;
	});
});


// Menu

$(document).ready(function() {

	var hoverDelay = 300;
	var hoverInID;
	var hoverOutID;

	function activateMenu() {
		var $mainmenu = $('.mainmenu-aim');
		var $menu = $('.submenu-aim');

		$mainmenu.menuAim({
			activate: activateMainSubmenu,
			deactivate: deactivateMainSubmenu,
			exitMenu: exitMainMenu,
			tolerance: 100,
			submenuDirection: 'below'
		});

		$menu.menuAim({
			activate: activateSubmenu,
			deactivate: deactivateSubmenu,
			exitMenu: exitMenu,
			submenuSelector: '.submenu'
		});

		// Set top content margin on pages with at least one level1
		// submenu selected
		if ($('.level1.current').length !== 0) {
			$('#content').css('margin-top', '144px');
		}

		// Set initial menu height
		setMenuHeight('selected', 'li.current-leaf ul');
	}

	function activateMainSubmenu(row) {
		hoverInID = setTimeout(function() {
			$(row).addClass('hover');
			if ($('.level0 > li.hover').not(row).length) {
				// Another top level menu is still open so we disable
				// the menu animations
				$(row).addClass('hover-notransition');
				$('.level0 > li.hover').not(row).removeClass('hover');
			}

			// Set the max-height of the .level1 based on the height of
			// the children ul (only for the default page menu)
			if ($(row).hasClass('current')) {
				var level1Current = $(row).find('.level1');
				var height = level1Current.children('ul').css('height');
				level1Current.css('max-height', height);
			}

		}, hoverDelay);

		setMenuHeight('selected', 'li.current-leaf ul');
	}

	function deactivateMainSubmenu(row) {
		clearTimeout(hoverInID);
		setMenuHeight('selected', 'li.current-leaf ul');

		// Reset level1 max-height
		$('.level1').css('max-height', '');
	}

	function exitMainMenu(submenu) {
		// If the highlighted menu is the current one we remove the hover
		// class straight to use the default css "hover out" animation
		if ($('.level0 > li.hover.current').length)
			$('.level0 > li.hover').removeClass('hover');
		else {
			hoverOutID = setTimeout(function() {
				$('.level0 > li.hover').removeClass('hover');
			}, hoverDelay);
		}

		$('.level0 > li.hover-notransition').removeClass('hover-notransition');

		return true;
	}

	function deactivateMenu() {
		var $menu = $('.submenu-aim').data('jquery.menuAim');

		if ($menu)
		{
			$menu.reset();
			$menu.destroy();
		}

		setMenuHeight('current-hover', 'li.hover > ul');
	}

	function activateSubmenu(row) {
		var $row = $(row),
			$submenu = $row.children('.sublevel'),
			$parent_menu = $row.parents('ul.submenu-aim');


		$parent_menu.find('.current .sublevel').addClass('hover');
		$parent_menu.addClass('current-hover');

		$row.addClass('hover');

		setMenuHeight('current-hover', 'li.hover > ul');

		// Show the submenu
		$submenu.css({
			display: 'block'
		});

		// Update the parent level1
		$submenu.closest('.level1').css('overflow', 'visible');
	}

	function deactivateSubmenu(row) {
		var $row = $(row),
			$parent_menu = $row.closest('ul.submenu-aim');

		$parent_menu.find('.current .sublevel').removeClass('hover');
		$parent_menu.removeClass('current-hover');
		$row.removeClass('hover');

		// Hide the submenu and remove the row's highlighted look
		$row.children('.sublevel').css('display', '');
		$row.closest('.level1').css('overflow', 'hidden');

		setMenuHeight('selected', 'li.current-leaf > ul');
	}

	function exitMenu(submenu) {
		var row = $(submenu.activeRow);
		deactivateSubmenu(row);
		return true;
	}

	// Close menu if click anywhere else
	$(document).on('click', function(event){
		if (!$(event.target).closest('.mainmenu-aim').length) {
			$('.sublevel').css('display', '');
			$('li.hover').removeClass('hover');
		}
	});

	enquire.register('screen and (min-width: 1025px)', {
		match: activateMenu,
		unmatch: deactivateMenu
	}, true);
});

function setMenuHeight(selector, leafSelector) {
	var height = 0;
	var leafChildren = 0;
	var maxChildren = 0;
	var menu = $('.main-menu ul.' + selector).first();

	while (menu.length > 0) {
		var nChildren = menu.children('li').length;
		if (nChildren > maxChildren)
			maxChildren = nChildren;

		if (menu.find('ul.' + selector).first().length)
			menu = menu.find('ul.' + selector).first();
		else
			break;
	}

	// Check if we are at a currently highlighted row, or a current-leaf with
	// children
	leafChildren = menu.find(leafSelector).children('li').length;
	if (leafChildren > maxChildren)
		maxChildren = leafChildren;

	$('.main-menu ul.' + selector).css('height', 25 * maxChildren + 30);
	if ($('.level0 > li.current.hover .level1').length) {
		$('.level0 > li.current.hover .level1').css('max-height', 25 * maxChildren + 30);
	}
}

$(document).ready(function() {
	let level1 = $('li.current > .level1-wrapper > div > ul');
	let liCount = level1.children('li').length;
	$('li.submenu.current > div > ul').each(function (idx, elm) {
		let current = $(elm).children('li').length;
		if (current > liCount)
			liCount = current;
	});
	level1.css('height', liCount * 25 + 30);
	$('.level0 > li').hover(function() {
	});
});


// Prepare PR carousel
$(document).ready(function(){
	$('#pr-carousel').slick({
		infinite: true,
		lazyLoad: 'progressive',
		prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>',
		autoplay: true,
		autoplaySpeed: 10000
	});
});

// Prepare Ann carousel
$(document).ready(function(){
	$('#ann-carousel').slick({
		infinite: false,
		lazyLoad: 'ondemand',
		slidesToShow: 4,
		slidesToScroll: 4,
		responsive: [
			{
				breakpoint: 970,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 3
				}
			},
			{
				breakpoint: 750,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
			},
			{
				breakpoint: 600,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
			}
		],
		prevArrow: '<button type="button" class="frontpage-slide-prev"><span class="fa fa-angle-left"></span</button>',
		nextArrow: '<button type="button" class="frontpage-slide-next"><span class="fa fa-angle-right"></span></button>',
		appendArrows: '.announcements .section-navigation'
	});
});


// Prepare POTW carousel
$(document).ready(function(){
	$('#potw-carousel').slick({
		infinite: false,
		lazyLoad: 'ondemand',
		prevArrow: '<button type="button" class="frontpage-slide-prev"><span class="fa fa-angle-left"></span</button>',
		nextArrow: '<button type="button" class="frontpage-slide-next"><span class="fa fa-angle-right"></span></button>',
		appendArrows: '#potw-carousel-wrapper .section-navigation'
	});
});


// Prepare Highlights carousel
$(document).ready(function(){
	$('#highlight-carousel').slick({
		infinite: true,
		lazyLoad: 'ondemand',
		autoplay: true,
		prevArrow: '<button type="button" class="frontpage-slide-prev"><span class="fa fa-angle-left"></span</button>',
		nextArrow: '<button type="button" class="frontpage-slide-next"><span class="fa fa-angle-right"></span></button>',
		appendArrows: '#highlight-carousel-wrapper .section-navigation'
	});
});


// Prepare Top100 frontpage carousel
$(document).ready(function(){
	$('#top100-frontpage-carousel').slick({
		infinite: false,
		lazyLoad: 'ondemand',
		prevArrow: '<button type="button" class="frontpage-slide-prev"><span class="fa fa-angle-left"></span</button>',
		nextArrow: '<button type="button" class="frontpage-slide-next"><span class="fa fa-angle-right"></span></button>',
		appendArrows: '#top100-frontpage-carousel-wrapper .section-navigation'
	});
});

// Prepare Top100 dedicated carousel
$(document).ready(function(){
	$('#top100-carousel').slick({
		infinite: true,
		lazyLoad: 'ondemand',
		prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>'
	});
});


function top100Fullscreen() {
	var elem = document.getElementById('top100-carousel-wrapper');
	if (elem.requestFullscreen) {
		elem.requestFullscreen();
	} else if (elem.msRequestFullscreen) {
		elem.msRequestFullscreen();
	} else if (elem.mozRequestFullScreen) {
		elem.mozRequestFullScreen();
	} else if (elem.webkitRequestFullscreen) {
		elem.webkitRequestFullscreen();
	}
}


// Prepare Pop-ups (previously shadowbox):
$(document).ready(function(){
	$('.archive-image.popup').each(function() {
			$(this).magnificPopup({
			type: 'image',
			delegate: 'a.popup',
			gallery: {
				enabled: true,
				preload: [1, 1]
			},
			mainClass: 'mfp-fade'
		});
	});

	$('.archive-image.popup-ajax').each(function() {
			$(this).magnificPopup({
			type: 'ajax',
			delegate: 'a.popup',
			closeBtnInside: true,
			mainClass: 'mfp-fade'
		});
	});

	$('.popup-youtube').each(function() {
		$(this).magnificPopup({
			type: 'inline',
			closeBtnInside: false,
			mainClass: 'mfp-fade',
			preloader: false
		});
	});

	$('.popup-jwplayer').each(function() {
		$(this).magnificPopup({
			type: 'inline',
			closeBtnInside: false,
			mainClass: 'mfp-fade',
			callbacks: {
				close: function() {
					console.log('Will remove');
					jwplayer('videoplayer').remove();
				}
			}
		});
	});
});

// Show/hide main search box
$('#searchbox-button').click(function(){
	$('.languages-dropdown').removeClass('active');
	$('#searchbox-dropdown').toggleClass('active');
	return false;
});

// Close main search box if click anywhere else
$(document).on('click', function(event){
	if (!$(event.target).closest('#searchbox-dropdown').length) {
		$('#searchbox-dropdown').removeClass('active');
	}
});


// images comparisons
$(window).load(function() {
	$('#before_after_container').beforeAfter( {
		animateIntro : true,
	    introDelay : 1000,
	    introDuration : 500,
	    showFullLinks : false,
	    imagePath : '/static/app/media/beforeafter/',
	    enableKeyboard : true
	});
});


function setWebcamTimestamp(selector, timestampPath) {
	$(selector + ':first').load(timestampPath, function(result) {
		var timestamp = $(selector + ':first').text().replace('\n', '');

		// Get the time difference in second between now and the pano timestamp:
		// We remove " CEST" from the string as javascript doesn't know how to
		// handle it and assume we're in local TZ anyway
		var timediff = (new Date - new Date(timestamp.replace(/ CES?T/, ''))) / 1000;

		// If more than 62 minutes we add a "not live" message
		var div = $(selector).parent('.webcam-timestamp').next('.webcam-live, .webcam-nolive');
		if (timediff > 3720) {
			div.text('Last image before nightfall');
			div.addClass('webcam-nolive');
			div.removeClass('webcam-live');

		} else {
			div.text('LIVE');
			div.addClass('webcam-live');
			div.removeClass('webcam-nolive');
		}

		// Set timestamp to all others .pano-timestamp
		$(selector).text(timestamp);

		// Add "webcam" to pano-timestamp within .webcam-wrapper
		$('.webcam-wrapper .pano-timestamp').text('Webcam | ' + timestamp);
	});
}


// Update Paranal panorama 'Live' in pages if any
// $(document).ready(function() {
	// if ($('.pano-timestamp').length) {
		// setWebcamTimestamp('.pano-timestamp', '/public/archives/static/pano/latest/timestamp.txt');
	// }
	// if ($('.hqcam-timestamp').length) {
		// setWebcamTimestamp('.hqcam-timestamp', '/public/archives/static/hqcam/timestamp.txt');
	// }
// });

function getJustifiedConfiguration(rowHeight, maxRowHeight, margin) {
	return {
		images : images,
		rowHeight: rowHeight,
		maxRowHeight: maxRowHeight,
		imageContainer: 'item',
		thumbnailPath: function(photo, width, height) {
			var purl = photo.src;
			if (height > 1000 || width > 900) {
				purl = purl.replace('/thumb300y/', '/screen/');
			} else if (height > 400) {
				purl = purl.replace('/thumb300y/', '/thumb700x/');
			}
			return purl;
		},
		getSize: function(photo) {
			return {width: photo.width, height: photo.height};
		},
		template: function(data) {
			var potw = '';
			if (data.potw) {
				potw = '<div class="potw" data-toggle="tooltip" data-placement="left" title="Picture of the Week, ' + data.potw + '">' +
					'<span class="fa fa-star"></span>' +
				'</div>';
			}
			// FIXME: the potw tooltip doesn't work because of the
			// "hover:after" div added in CSS to show the blue box-shadow

			return '<a href="' + data.url + '" class="item" style="height:' + data.displayHeight + 'px;margin-right:' + data.marginRight + 'px;">' +
				'<img class="image-thumb" style="width:' + data.displayWidth + 'px;height:' + data.displayHeight + 'px;" src="' + data.src + '" alt="' + data.title + '" />' +
				'<div class="title">' + data.title + '</div>' + potw +
			'</a>';
		},
		margin: margin
	};
}

function setupJustified(selector, width, height, margin) {
	var window_width;
	function run() {
		$(selector).empty().justifiedImages(
			getJustifiedConfiguration(width, height, margin)
		);
		window_width = $(window).width();
	}

	if ($(selector).length) {
		run();

		$(window).resize(function() {
			// Re-justify if the window widht has changed
			if ($(window).width() != window_width) {
				run();
			}
		});
	}
}

setupJustified('.image-list-300', 400, 600, 8);
setupJustified('.image-list-200', 200, 500, 8);
setupJustified('.image-list-150', 150, 600, 8);


// Load tooltips and popover if any
$('[data-toggle="tooltip"]').tooltip();

// Load popover if any
$('[data-toggle="popover"]').popover();

// Close popover when click outside
$('body').on('click', function (e) {
    $('[data-toggle=popover]').each(function () {
        // hide any open popovers when the anywhere else in the body is clicked
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
            $(this).popover('hide');
        }
    });
});


// Setup Masonry on archive list page
$(window).load(function() {
	if ($('.archive-list').length) {
		$('.archive-list').each(function() {
			var msnry = new Masonry(this, {
				itemSelector: '.item',
				columnWidth: '.item',
				transitionDuration: 0
			});
		});
	}
});


// Set default settings for jwplayer:
let jwplayer_ga = {idstring: 'UA-2368492-6'};
const jwplayer_html5player = '/static/app/djangoplicity/jwplayer/jwplayer.html5.js';
const jwplayer_flashplayer = '/static/app/djangoplicity/jwplayer/jwplayer.flash.swf';
