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
      const viewBox = `0 0 ${this.width} ${this.height}`;
      // TODO (codeviking): Replace with actual polygons
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
