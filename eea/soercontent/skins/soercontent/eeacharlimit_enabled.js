/*charlimit_options object needed for eeacharlimit tinymce plugin
 - ctype defines the content type name
 - fields is an array of the rich fields we should be active on
 - threshold defines the character limit
 */

if(window.eeacharlimit_options === undefined){
  var eeacharlimit_options = {};
}

eeacharlimit_options.fiche = {
    ctype: 'fiche',
    fields:['text'],
    threshold: 8000
};
