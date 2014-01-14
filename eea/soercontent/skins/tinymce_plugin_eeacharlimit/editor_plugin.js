/*This plugin is based on Adam Scheller's tinymce count characters plugin:
http://adamscheller.com/tinymce-count-characters-plugin/

This plugin is counting the characters entered in a fiche's RichWidget fields.
In order for the plugin to be active, a eeacharlimit_options javascript object
needs to be present and the content type, richwidget fields and threshold need 
to be defined.
 */
/*global jQuery, tinymce, eeacharlimit_options */

if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function(obj, start) {
         'use strict';
         for (var i = (start || 0), j = this.length; i < j; i++) {
             if (this[i] === obj) { return i; }
         }
         return -1;
    };
}

(function() {
    'use strict';
    tinymce.create('tinymce.plugins.EEACharLimitPlugin', {
        init : function(ed) {
            var self = this;

            //Update the status_box with the required info
            function status_update(status_box, threshold) {
                var message;
                var char_num = self.getCountCharacters();

                if (char_num <= threshold) {
                    var under_threshold = threshold - char_num;
                    message = under_threshold + ' characters left.';

                    if (status_box.hasClass('charlimit-exceeded')) {
                        status_box.removeClass('charlimit-exceeded');
                    }
                } else {
                    var over_threshold = char_num - threshold;
                    message = 'Please remove ' + over_threshold + ' characters.';

                    if (!status_box.hasClass('charlimit-exceeded')) {
                        status_box.addClass('charlimit-exceeded');
                    }
                }

                status_box.text(message);
            }

            function add_placeholder(parent_id, elem) {
                var parent = jQuery('#' + parent_id);
                var tiny_table = parent.find(jQuery('table[role="presentation"][class~="mceLayout"'));

                tiny_table.find('tr[class="mceFirst"]').after(elem);
            }

            ed.onInit.add(function() {

                //Check for eeacharlimit_options object
                if (typeof eeacharlimit_options != 'undefined') {

                    jQuery.each(eeacharlimit_options, function( index, value ) {
                        var body_class = jQuery('body').attr('class');
                        var marker = 'portaltype-' + value.ctype;
                        var field_id = ed.editorId;
                        var row_id = 'charlimit-row-' + field_id;

                        //If we're in fullscreen mode, check which field we're editing
                        if (ed.getParam('fullscreen_is_enabled')) {
                            field_id = ed.getParam('fullscreen_editor_id');
                            row_id = 'charlimit-row-' + field_id;
                        }

                        //Check if we should activate for this CT and field
                        if (body_class.indexOf(marker) >= 0 && value.fields.indexOf(field_id) >=0 ) {
                            var threshold = value.threshold;
                            var char_left = threshold - self.getCountCharacters();
                            var tinymce_row = jQuery('#' + row_id);
                            var status_box = jQuery('#info-' + field_id);

                            // Check if we have our custom row
                            if (tinymce_row.length === 0) {
                                tinymce_row = jQuery('<tr />', {
                                    'class': 'charlimit-row',
                                    'id': 'charlimit-row-' + field_id
                                });
                            }

                            // Check if we have our status_box
                            if (status_box.length === 0) {
                                status_box = jQuery('<div />', {
                                    'class': 'charlimit-info',
                                    'id': 'info-' + field_id,
                                    'text': char_left + ' characters left.'
                                });
                                tinymce_row.append(status_box);
                            }
                            
                            add_placeholder(ed.editorContainer, tinymce_row);

                            ed.onKeyUp.add(function() {
                                status_update(status_box, threshold);
                            });

                            // Redraw our custom tinymce table row when exiting fullscreen
                            ed.onBeforeExecCommand.add(function(ed, cmd) {
                                if (cmd === 'mceFullScreen') {
                                    if (ed.getParam('fullscreen_is_enabled')) {
                                        var orig_field = ed.getParam('fullscreen_editor_id');
                                        var container = tinymce.getInstanceById(orig_field).editorContainer;
                                        add_placeholder(container, tinymce_row);
                                    }
                                }
                            });
                        }
                    });
                }
            });
            
            //Count the characters entered by the user, strip out the html and convert
            //chars like &nbsp to a single character
            self.getCountCharacters = function() {
                var strip = ed.getContent({format: 'raw'}).replace(/<.[^<>]*?>/g, '').replace(/&[^;]+;/g, '?');
                return strip.length;
                };
            },

        getInfo : function() {
            return {
                longname : 'TinyMCE Character limit',
                author : 'Olimpiu Rob',
                authorurl : '',
                infourl : '',
                version : tinymce.majorVersion + '.' + tinymce.minorVersion
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('eeacharlimit', tinymce.plugins.EEACharLimitPlugin);
})();
