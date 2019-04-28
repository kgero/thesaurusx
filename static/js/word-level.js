
var STOP_STRING = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your'
var STOP_LIST = STOP_STRING.split(',')

// return string with punctuation removed
function clean(thisString) {
  return thisString.replace(/\n|'|\(|\)|,|\./g, '')
}

// add synonym tooltips to all words in all divs IN div
function add_tooltips(div) {
  div.children().each(function(index, item) {
    var words = $(item).text().split(" ");
    $(item).empty();
    // var p = $('<p>');
    $.each(words, function(i, v) {
      if (v.length > 0) {
        var sp = $("<span>").text(v);
        if (STOP_LIST.indexOf(v) < 0) {
          sp.click( function() { get_full_response(clean(v)); });
          sp.addClass(clean(v));
          sp.addClass('ok-word');
          sp.attr('data-toggle', 'tooltip');
          sp.attr('data-placement', 'top');
          sp.attr('title', 'none yet');

          sp.attr('data-template', '<div class="tooltip" role="tooltip"><div class="tooltip-inner"></div></div>');
          // sp.attr('data-trigger', 'click')
          $(item).append(sp);
          $(item).append(' ');
          $('[data-toggle="tooltip"]').tooltip();
          real_simple_lookup(clean(v));
        } else {
          $(item).append(sp);
          $(item).append(' ');
        }
      };
    });
    // $(item).append(p);
  });
  
  console.log('added tooltips')
}

// put query and full response in more-responses div
function get_full_response(word) {
  console.log('clikced!');
  data = {keyword: word, n: 10, embkey: 'arxiv_abs_lemma'}
  $.post('real_simple_lookup?', data, function(json, status) {
    // console.log('simple response:', json);
    if (json.hasOwnProperty('error')) { var resp = json.error; }
    else { var resp = json['words'].join(', '); }
    $('.more-response').prepend('<p>'+resp+'</p>');
    $('.more-response').prepend('<p><strong>'+word+'</strong></p>')
    
  });
}

// lookup synonyms for word and add those synonyms to tooltip for
// any DOM with class=word
function real_simple_lookup(word) {
  if (word.length == 0) { 
    console.log('error, looked up empty string');
    return }
  data = {keyword: word, embkey: 'arxiv_abs_lemma'}
  $.post('real_simple_lookup?', data, function(json, status) {
    if (json.hasOwnProperty('error')) { var tip = json.error; }
    else { var tip = json['words'].join(' '); }
    $('.' + clean(word)).attr('data-original-title', tip);
    $('[data-toggle="tooltip"]').tooltip();
  });
}

$(document).ready( function() {
  $.fn.tooltip.Constructor.prototype.getCalculatedOffset = function (placement, pos, actualWidth, actualHeight) {
        return placement === 'bottom' ? {
                top: pos.top + pos.height,
                left: pos.left + pos.width / 2 - actualWidth / 2 } :
            placement === 'top' ? {
                top: pos.top - actualHeight + 3,  // my fix!!!
                left: pos.left + pos.width / 2 - actualWidth / 2 } :
            placement === 'left' ? {
                top: pos.top + pos.height / 2 - actualHeight / 2,
                left: pos.left - actualWidth } :
            /* placement == 'right' */ {
                top: pos.top + pos.height / 2 - actualHeight / 2,
                left:
                    /* begin fix */
                    Math.min(
                        pos.left + pos.width, //original left
                        $(".inner-container").offset().left + $(".inner-container")[0].clientWidth //max left
                    )
                    /* end fix */
            };
    };

  console.log('booting up...');

  add_tooltips($('.texthere'))

  $('.update').click( function() {
    add_tooltips($('.texthere'))
  });

});
