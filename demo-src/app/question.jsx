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

class Question extends React.Component {
  render() {
    return (
      <div className="question flex-row">
        <img src={`assets/${this.props.questionKey}/diagram.png`} />
        <div className="question-text">
          {this.props.text}
          <QuestionChoiceList choices={this.props.choices} selected={this.props.selected} />
        </div>
      </div>
    );
  }
}

module.exports = Question;
