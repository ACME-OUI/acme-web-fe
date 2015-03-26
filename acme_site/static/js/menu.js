$('body').ready(function(){
/***********************************
        Left slide menu
***********************************/
  var body = document.body,
      mask = document.createElement('div'),
      toggleSlideLeft = document.querySelector('.toggle-slide-left');

  mask.className = 'mask';

  $(toggleSlideLeft).click(function() {
    $(body).addClass('sml-open');
    document.body.appendChild(mask);
  });

  /* hide active menu if mask is clicked */
  $(mask).click(function(){
    $(body).removeClass('sml-open');
    document.body.removeChild(mask);
  });

  $('.close-menu').click(function(){
    $(body).removeClass('sml-open');
    document.body.removeChild(mask);
  });

  $('#toggle-slide-left').click(function(e){
    $('#slide-menu-left').animate({width: 'toggle'}, 500, 'linear');
    if( $('#toggle-left-a').text() == 'Window Menu') {
      $('#toggle-left-a').text('Close Menu');
    } else {
      $('#toggle-left-a').text('Window Menu');
    }
  });

/**********************************
       Top slide down menu
**********************************/

  $('#drop-down-tab').click(function(e){
    var menuHeight = parseInt($('#drop-down-menu').css('height'));
    if($('#drop-down-menu').css('display') == 'none'){
      $('.tile').each(function(){
        $(this).css({
          'top':parseInt($(this).css('top'))+menuHeight
        });
      });
    } else {
      $('.tile').each(function(){
        $(this).css({
          'top':parseInt($(this).css('top'))-menuHeight
        });
      });
    }
    $('#drop-down-menu').slideToggle('normal');
  });
});