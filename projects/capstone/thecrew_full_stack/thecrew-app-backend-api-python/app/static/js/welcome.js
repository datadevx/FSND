jQuery(document).ready(function ($) {

  // Header fixed and Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 10) {
      $('#header').addClass('header-fixed');
    } else {
      $('#header').removeClass('header-fixed');
    }

    var target = $(this.hash);
    if (target.length) {
      var top_space = 0;

      if ($('#header').length) {
        top_space = $('#header').outerHeight();

        if (!$('#header').hasClass('header-fixed')) {
          top_space = top_space - 20;
        }
      }

      $('html, body').animate({
        scrollTop: target.offset().top - top_space
      }, 1500, 'easeInOutExpo');
      return false;
    }
  });

  // Initiate the AOS animation library
  AOS.init();

  // custom code

});
