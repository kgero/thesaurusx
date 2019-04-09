

function add_tooltips(div) {
  var words = div.text().split(" ");
  div.empty();
  $.each(words, function(i, v) {
    if (v.length > 0) {
      var sp = $("<span>").text(v);
      sp.addClass(v);
      sp.attr('data-toggle', 'tooltip');
      sp.attr('data-placement', 'top');
      sp.attr('title', 'none yet');
      div.append(sp);
      div.append(' ');
      $('[data-toggle="tooltip"]').tooltip();
      real_simple_lookup(v)
      
    };
  });
  
  console.log('added tooltips')
}

function real_simple_lookup(word) {
  data = {keyword: word, embkey: 'arxiv_abs_lemma'}
  // console.log(data);
  $.post('real_simple_lookup?', data, function(json, status) {
    console.log('simple response:', json);
    if (json.hasOwnProperty('error')) { var tip = 'not in vocab'; }
    else { var tip = json['words'].join(' '); }
    $('.' + word).attr('data-original-title', tip);
    $('[data-toggle="tooltip"]').tooltip();
    console.log('updated', word);
  });
}

$(document).ready( function() {

  console.log('booting up...');

  add_tooltips($('.texthere'))

  real_simple_lookup('test')

  $('.update').click( function() {
    add_tooltips($('.texthere'))
  });

});
