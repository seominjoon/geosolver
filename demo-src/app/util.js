'use strict';

const prefixes = [ 'Moz', 'Webkit', 'Ms', 'O' ];

module.exports = {
  prefixed: (prop, value) => {
    var styles = {};
    [ prop ].concat(prefixes.map((prefix) => {
      const propertyName = prefix + prop.substr(0, 1).toUpperCase() + prop.substr(1);
      styles[propertyName] = value;
    }));
    return styles;
  }
};
