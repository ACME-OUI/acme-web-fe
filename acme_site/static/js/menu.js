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
    $('#slide-menu-left').toggle('slide','linear', 500);
    // $('#slide-menu-left').animate({width: 'toggle'}, 'slow', 'linear');
    if( $('#toggle-left-a').text() == 'Open Menu') {
      $('#toggle-left-a').text('Close Menu');
    } else {
      $('#toggle-left-a').text('Open Menu');
    }
  });

  $('#dark-mode-toggle').click(function(e){
    if($('body').attr('class') == 'day'){
      //turn dark
      $('body').attr({
        'class':'night'
      });
      $('.tile-panel-body').each(function(){
        $(this).css({
          'background-color': '#051451!;',
          'border-color': '#00f;'
        });
      });
      $(body).attr({
        'background-color':'#051451!important',
        'color':'#aaa!important'
      });
      $('#dark-mode-toggle').text('Dark mode is on');
    } else {
      //turn light
      $('body').attr({
        'class':'day'
      });
      $('.tile-panel-body').each(function(){
        $(this).css({
          'background-color': '#fff;',
          'color': '#111;',
          'border-color': '#000;'
        });
      });
      $(body).attr({
        'background-color':'#fff',
        'color':'#000'
      });
      $('#dark-mode-toggle').text('Dark mode is off');
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