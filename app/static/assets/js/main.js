var header = document.querySelector('header');
var body = document.body;
var progressBar = document.querySelector('.progress-bar .bar');

if(progressBar) {
	function scrollIndicator() {
		var pixelScrolled = window.scrollY;
		var viewportHeight = window.innerHeight;
		var totalHeightScrollable = body.scrollHeight;
		var pixelsToPercentage =
		(pixelScrolled / (totalHeightScrollable - viewportHeight)) * 100;
		progressBar.style.width = pixelsToPercentage + '%';
	}
}

function headerInteraction() {
	var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
	if( scrollTop > 0 ) {
		header.classList.add('show-bg');
	} else {
		header.classList.remove('show-bg');
	}
}

headerInteraction();

window.addEventListener('scroll', function() {
	headerInteraction();
	if(progressBar) scrollIndicator();
});

var burgerMenu = document.querySelector('.burger-menu');
burgerMenu.addEventListener('click', function() {
	header.classList.toggle('show-nav');
});

// popup
var openPopupTrigger = document.querySelectorAll('.open-popup-trigger');
var closePopupTrigger = document.querySelectorAll('.close-popup-trigger');

openPopupTrigger.forEach(function(button) {
	button.addEventListener('click', function(e) {
		e.preventDefault();
		popup.classList.add('is-active');
	});
});

closePopupTrigger.forEach(function(button) {
	button.addEventListener('click', function(e) {
		e.preventDefault();
		closePopup();
	});
});

function closePopup() {
	popup.classList.remove('is-active');
}

body.addEventListener('keyup', function(e) {
	if(e.keyCode == 27) {
		closePopup();
	}
})

// scroll animations
function animFly(items, options) {

	TweenMax.staggerFrom(items, options.duration, {
		delay: options.delay,
		y: options.y,
		ease: Power4.easeOut
	}, options.repeatDelay)
	TweenMax.staggerTo(items, options.duration, {
		delay: options.delay,
		opacity: 1
	}, options.repeatDelay)

}

// stagger animation
var staggerAnims = document.querySelectorAll('.stagger-animation');
var yAnim = 15;
if(staggerAnims) {

	staggerAnims.forEach(function(anim) {
		var animItems = anim.querySelectorAll('.anim-item');

		var animWatcher = scrollMonitor.create(anim, -250);
		var animScroll = anim.getAttribute('data-scroll');
		var animState = false;

		if(animScroll == 'false') {

			animFly(animItems, {
				duration: .85,
				delay: .3,
				y: yAnim,
				repeatDelay: .2
			})
			animState = true;

		} else {

			animWatcher.enterViewport(function() {
				if(!animState) {
					animFly(animItems, {
						duration: .85,
						delay: 0,
						y: yAnim,
						repeatDelay: .2
					})
					animState = true;
				}
			})

		}

	});

}