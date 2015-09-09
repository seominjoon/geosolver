'use strict';

const React = require('react');

class QuestionChoiceList extends React.Component {
  render() {
    let choices = [];
    for (let key in this.props.choices) {
      if (this.props.choices.hasOwnProperty(key)) {
        const isSelected = parseInt(key, 10) === parseInt(this.props.selected, 10);
        const className = isSelected ? 'is-selected flex-row' : '';
        const icon = isSelected ? <span className="flex-right icon-check"></span> : '';

        choices.push(
          <li key={key} className={className}>
            <span>
              ({String.fromCharCode(parseInt(key, 10) + 64)})
              &nbsp;{this.props.choices[key].replace('*\\degree', '°')}
            </span>
            {icon}
          </li>
        );
      }
    }
    return <ul className="question-choice-list">{choices}</ul>;
  }
}

class SemanticTreeNode {
  constructor(content, children) {
    this.content = content;
    this.children = children;
  }

  toString() {
    var out = this.content.toString();
    if (this.children.length === 0) {
      return out;
    }
    out += "(";
    for (var i = 0; i < this.children.length; i++) {
      out += this.children[i].toString();
    }
    out += ")";
    return out;
  }

  getTagRules() {
    var out = [this.content];
    for (var i = 0; i < this.children.length; i++) {
      out = out.concat(this.children[i].getTagRules());
    }
    return out;
  }
}

function dictToSemanticTreeNode(dict, sentence_number) {
  var content = dictToTagRule(dict.content, sentence_number);
  var children = [];
  for (var i = 0; i < dict.children.length; i++) {
    children.push(dictToSemanticTreeNode(dict.children[i], sentence_number));
  }
  var stn = new SemanticTreeNode(content, children);
  return stn;
}

class TagRule {
  constructor(sentence_number, span, signature) {
    this.sentence_number = sentence_number;
    this.span = span;
    this.signature = signature;
  }

  toString() {
    return this.signature.toString();
  }

  getKey() {
    return this.sentence_number.toString() + "_" + "_" + this.signature.getKey();
  }
}

function dictToTagRule(dict, sentence_number) {
  var signature = dictToSignature(dict.signature);
  return new TagRule(sentence_number, dict.span, signature);
}

class FunctionSignature {
  constructor(id, return_type, arg_types, name) {
    this.id = id;
    this.return_type = return_type;
    this.arg_types = arg_types;
    this.name = name;
  }

  toString() {
    return this.return_type + " " + this.name;
  }

  getKey() {
    return this.id.toString();
  }
}

class VariableSignature {
  constructor(id, return_type, name) {
    this.id = id;
    this.return_type = return_type;
    this.name = name;
  }

  toString() {
    return this.return_type + " " + this.name;
  }

  getKey() {
    return this.id.toString();
  }
}

function dictToSignature(dict) {
  if (dict.class === "FunctionSignature") {
    return new FunctionSignature(dict.id, dict.return_type, dict.arg_types, dict.name);
  } else {
    return new VariableSignature(dict.id, dict.return_type, dict.name);
  }
}

function listToEntityMap(list) {
  var map = {};
  for (var i = 0; i < list.length; i ++) {
    var curr = list[i];
    var tagRule = dictToTagRule(curr.content, curr.sentence_number);
    map[tagRule.getKey()] = curr.coords;
  }
  return map;
}

function getSvg(tagRule, coords) {
  let svg;
  if (tagRule.signature.return_type === "circle") {
    svg = (
        <circle cx={coords[0][0]} cy={coords[0][1]} r={coords[1]} />
    );
  } else if (tagRule.signature.return_type == "line"){
    svg = (
        <line x1={coords[0][0]} y1={coords[0][1]} x2={coords[1][0]} y2={coords[1][1]} />
    );
  } else if (tagRule.signature.return_type == "point") {
    svg = (
        <circle cx={coords[0]} cy={coords[1]} r="5" />
    );
  } else {
    const string = coords.map(function(point) {
      return point.join(",");
    }).join(" ");
    svg = (
        <polygon points={string} />
    );
  }
  return svg;
}

const PATTERN_KEYWORDS = /\(([^()]+)\)/;
const PATTERN_PARENS = /[()]/;

class Question extends React.Component {

  componentDidMount() {
    const container = React.findDOMNode(this.refs.diagramContainer);
    this.width = container.offsetWidth;
    this.height = container.offsetHeight;
  }

  render() {

    let svg;
    let text = this.props.text;
    if(this.props.activeFormula) {
      var tree = dictToSemanticTreeNode(this.props.activeFormula.tree, this.props.activeFormula.sentence_number);
      let tagRules = tree.getTagRules();
      var entityMap = listToEntityMap(this.props.entityMap);
      console.log(tagRules);
      let svgs = tagRules.map(function(tagRule) {
        if (tagRule.getKey() in entityMap) {
          console.log(entityMap[tagRule.getKey()]);
          return getSvg(tagRule, entityMap[tagRule.getKey()]);
        } else {
          return "";
        }
      });
      console.log(svgs);
      const viewBox = `0 0 ${this.width} ${this.height}`;
      svg = (
          <svg viewBox={viewBox} width={this.width} height={this.height}>
            // TODO (seominjoon): How to show multiple svgs?
            {svgs[1]}
          </svg>
      );

      /*
      const random = Math.random();
      if (random >= 0.75) {
        svg = (
          <svg viewBox={viewBox} width={this.width} height={this.height}>
            <polygon points="60,20 100,40 100,80 60,100 20,80 20,40" />
          </svg>
        );
      } else if (random < 0.75 && random >= 0.5) {
        svg = (
          <svg viewBox={viewBox} width={this.width} height={this.height}>
            <line x1="0" y1="0" x2="200" y2="200" />
          </svg>
        );
      } else if (random < 0.5 && random >= 0.25) {
        svg = (
          <svg viewBox={viewBox} width={this.width} height={this.height}>
            <rect x="10" y="10" width="100" height="100"/>
          </svg>
        );
      } else {
        svg = (
          <svg viewBox={viewBox} width={this.width} height={this.height}>
            <circle cx="50" cy="50" r="40" />
          </svg>
        );
      }
      */

      const keywords =
        this.props.activeFormula.simple.match(PATTERN_KEYWORDS)
            .pop()
            .replace(PATTERN_PARENS, '')
            .split(',');

      if (keywords.length > 0) {
        keywords.forEach((keyword) => {
          const index = text.indexOf(keyword);
          if (index >= 0) {
            text = [
              text.substring(0, index),
              `<span class="is-active-text">${keyword}</span>`,
              text.substring(index + keyword.length)
            ].join('');
          }
        });
      }
    }

    return (
      <div className="question flex-row">
        <div className="question-diagram-container" ref="diagramContainer">
          <img src={`assets/${this.props.questionKey}/diagram.png`} />
          {svg}
        </div>
        <div className="question-text">
          <div dangerouslySetInnerHTML={{__html: text}} />
          <QuestionChoiceList choices={this.props.choices} selected={this.props.selected} />
        </div>
      </div>
    );
  }
}

module.exports = Question;
