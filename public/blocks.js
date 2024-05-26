Blockly.common.defineBlocksWithJsonArray([{
  "type": "startblock",
  "message0": "ON START",
  "nextStatement": null,
  "colour": 0,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "ifstatement",
  "message0": "IF %1 THEN %2",
  "args0": [
    {
      "type": "input_value",
      "name": "IF"
    },
    {
      "type": "input_statement",
      "name": "THEN"
    }
  ],
  "inputsInline": true,
  "previousStatement": null,
  "nextStatement": null,
  "colour": 315,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "ifelsestatement",
  "message0": "IF %1 THEN %2 ELSE %3",
  "args0": [
    {
      "type": "input_value",
      "name": "IF"
    },
    {
      "type": "input_statement",
      "name": "THEN"
    },
    {
      "type": "input_statement",
      "name": "ELSE"
    }
  ],
  "inputsInline": true,
  "previousStatement": null,
  "nextStatement": null,
  "colour": 315,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "variable",
  "message0": "VAR %1",
  "args0": [
    {
      "type": "field_input",
      "name": "VARNAME",
      "text": "Variable Name"
    }
  ],
  "inputsInline": true,
  "output": null,
  "colour": 60,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "equivalence",
  "message0": "%1 == %2",
  "args0": [
    {
      "type": "input_value",
      "name": "NAME"
    },
    {
      "type": "input_value",
      "name": "NAME"
    }
  ],
  "inputsInline": true,
  "output": null,
  "colour": 180,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "setting",
  "message0": "%1 = %2 %3",
  "args0": [
    {
      "type": "input_value",
      "name": "NAME"
    },
    {
      "type": "input_dummy"
    },
    {
      "type": "field_input",
      "name": "NEWVAL",
      "text": "0"
    }
  ],
  "inputsInline": true,
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "const",
  "message0": "CONST %1",
  "args0": [
    {
      "type": "field_input",
      "name": "CONSTVAL",
      "text": "0"
    }
  ],
  "output": null,
  "colour": 60,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "mathconst",
  "message0": "%1 %2 %3 %4",
  "args0": [
    {
      "type": "input_value",
      "name": "A"
    },
    {
      "type": "field_dropdown",
      "name": "operation",
      "options": [
        [
          "+",
          "ADD"
        ],
        [
          "-",
          "SUB"
        ],
        [
          "*",
          "MULT"
        ],
        [
          "/",
          "DIV"
        ],
        [
          "^",
          "POW"
        ]
      ]
    },
    {
      "type": "input_dummy"
    },
    {
      "type": "field_input",
      "name": "Mathval",
      "text": "0"
    }
  ],
  "inputsInline": true,
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "mathvar",
  "message0": "%1 %2 %3 %4",
  "args0": [
    {
      "type": "input_value",
      "name": "A"
    },
    {
      "type": "field_dropdown",
      "name": "operation",
      "options": [
        [
          "+",
          "ADD"
        ],
        [
          "-",
          "SUB"
        ],
        [
          "*",
          "MULT"
        ],
        [
          "/",
          "DIV"
        ],
        [
          "^",
          "POW"
        ]
      ]
    },
    {
      "type": "input_dummy"
    },
    {
      "type": "input_value",
      "name": "B"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
}]);