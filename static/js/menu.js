$('body').ready(function(){
/***********************************
        Left slide menu
***********************************/
  var body = document.body;

  function leftMenuToggle(){
    $('#slide-menu-left').animate({
      width: '200px'
    });
    if( $('#toggle-left-a').text() == 'Open Menu') {
      $('#toggle-left-a').text('Close Menu');
    } else {
      $('#toggle-left-a').text('Open Menu');
    }
  }

  $('#toggle-slide-left').click(function(e){
    leftMenuToggle();
  });

  $('#save-layout').click(function(){
    leftMenuToggle();
    var mask = document.createElement('div');
    $(mask).addClass('mask');
    $(mask).attr({'id':'mask'});
    $(mask).click(function(){
      $(this).fadeOut().queue(function(){
        $(this).remove();
        $('.save-layout').remove();
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

    var options = [{ //placeholder
      name : 'science',
      mode: 'day',
      style: 'balanced',
      layout: 
        [{ 
          tileName:'scince_window',
          x:'1',
          y:'1',
          sizex:'max',
          sizey:'max'
        }]
      },{
      name:'run',
      mode: 'night',
      style: 'balanced',
      layout:
        [{
          tileName:'status_window',
          x:'1',
          y:'1',
          sizex:'3',
          sizey:'max'
        },{
          tileName:'modelRun_window',
          x:'4',
          y:'1',
          sizex:'max-3',
          sizey:'max'
        }] 
      }
    ]; 
    leftMenuToggle();
    var mask = document.createElement('div');
    $(mask).addClass('mask');
    $(mask).attr({'id':'mask'});
    $(mask).click(function(){
      $(this).fadeOut().queue(function(){
        $(this).remove();
        $('.save-layout').remove();
      });
    });
    $('body').append(mask);
    var loadMenu = document.createElement('div');
    $(loadMenu).addClass('bvc');
    $(loadMenu).addClass('save-layout');
    var loadMenuHtml = '<div class="bevel tl tr"></div><div class="content">'
    loadMenuHtml += '<form name="load-layout-form" id="save-form">'; 
    loadMenuHtml += 'Select Layout:<br><select id="select-layout">';
    for (var i = options.length - 1; i >= 0; i--) {
      loadMenuHtml += '<option value="' + options[i].name + '">' + options[i].name + '</option>';
    }
    loadMenuHtml += '</select><input type="submit" value="Load" id="load-button">';
    loadMenuHtml += '</form></div><div class="bevel bl br"></div>';
    $(loadMenu).html(loadMenuHtml);
    $('body').append(loadMenu);
    $(mask).fadeIn();
    $('#load-button').click(function(){
      var name = document.forms['load-layout-form'].elements[0].options[document.forms['load-layout-form'].elements[0].selectedIndex].text;
      for(var i = 0; i < options.length; i++){
        if(name == options[i].name){
          loadLayout(options[i]);
        }
      }
    });
  });

  function loadLayout(layout){
    if(layout.mode == 'day'){
      setDay();
    }
    else if(layout.mode == 'night'){
      setNight();
    }

    for(var i = 0; i < layout.layout.length; i++){
      var t = add_tile(layout.layout[i].tileName);
    }


  }

  function setNight(){
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
  }

  function setDay(){
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


  $('#dark-mode-toggle').click(function(e){
    if($('body').attr('class') == 'day'){
      //turn dark
      setNight();
    } else {
      //turn light
      setDay();
    }
  });

/**********************************
       Top slide down menu
**********************************/

  $('#drop-down-tab').click(function(e){

    var menuHeight = parseInt($('#drop-down-menu').css('height'));
    // $.ajax({
    //   url:'node_layout/',
    //   type: 'GET',
    //   async: true,
    //   cache: false,
    //   statusCode: {
    //     500: function(){
    //       alert('Unable to retrieve node information');
    //     }
    //   },
    //   success: function(response){
    //     nodeInfo = jQuery.parseJSON(response);
    //     console.log(nodeInfo);
    //   }
    // });
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
    $('.node-carousel').slick({
      infinite: true,
      slidesToShow: 3,
      slidesToScroll: 1,
    });
  });


  /**
   * This is a stub. Currently it loads dummy data from a local file. When the node manager is ready it will get the current data from there
   *
   */
  function loadNodeInfo(){
    $.ajax({
      url:'node_layout/',
      type: 'GET',
      async: true,
      cache: false,
      statusCode: {
        500: function(){
          alert('Unable to retrieve node information');
        }
      },
      success: function(response){
        nodeInfo = jQuery.parseJSON(response);
        console.log(nodeInfo);
      }
    });
  }
});