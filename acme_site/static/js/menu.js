$('body').ready(function(){
/***********************************
        Left slide menu
***********************************/
  var body = document.body;


  $('#toggle-slide-left').click(function(e){
    $('#slide-menu-left').toggle('slide',{
      direction: 'left',
      easing: 'easeOutCubic'}, 500);
    if( $('#toggle-left-a').text() == 'Open Menu') {
      $('#toggle-left-a').text('Close Menu');
    } else {
      $('#toggle-left-a').text('Open Menu');
    }
  });

  $('#save-layout').click(function(){
    $(this).prop('disabled', true);
    var mask = document.createElement('div');
    $(mask).addClass('mask');
    $(mask).attr({'id':'mask'});
    $(mask).click(function(){
      $(this).fadeOut().queue(function(){
        $(this).remove();
        $('.save-layout').remove();
        $('#save-layout').prop('disabled', false);
      });
      
    });
    $('body').append(mask);
    
    var saveMenu = document.createElement('div');
    $(saveMenu).addClass('bvc');
    $(saveMenu).addClass('save-layout');
    var saveMenuHtml = '<div class="bevel tl tr"></div><div class="content">'
    saveMenuHtml += '<form name="save-layout-form" id="save-form">'; 
    saveMenuHtml += 'Layout Name:<br><input type="text" name="layout-name">';
    saveMenuHtml += '<input type="submit" value="Save">';
    saveMenuHtml += '</form></div><div class="bevel bl br"></div>';
    $(saveMenu).html(saveMenuHtml);
    $('body').append(saveMenu);
    $(mask).fadeIn();
  });


  $('#load-layout').click(function(){
    $(this).prop('disabled', true);
    var mask = document.createElement('div');
    $(mask).addClass('mask');
    $(mask).attr({'id':'mask'});
    $(mask).click(function(){
      $(this).fadeOut().queue(function(){
        $(this).remove();
        $('.load-layout').remove();
        $('#load-layout').prop('disabled', false);
      });
    });
    $('body').append(mask);
    /*

    Do some stuff

    */
  });



  $('#dark-mode-toggle').click(function(e){
    if($('body').attr('class') == 'day'){
      //turn dark
      $('body').attr({
        'class':'night'
      });
      $('.tile-panel-body').each(function(){
        $(this).css({
          'background-color': '#0C1021;',
          'border-color': '#00f;',
          'color': '#fff'
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