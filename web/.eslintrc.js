/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2020, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

module.exports = {
  'env': {
    'browser': true,
    'es6': true,
    'amd': true,
    'jasmine': true,
  },
  'extends': [
    'eslint:recommended',
  ],
  'parserOptions': {
    'ecmaVersion': 2018,
    'sourceType': 'module',
  },
  'plugins': [
  ],
  'globals': {
    '_': true,
    'module': true,
  },
  'rules': {
    /*'indent': [
      'error',
      2
    ],*/
    'linebreak-style': 0,
    /*'quotes': [
      'error',
      'single'
    ],*/
    'quotes': 'off',
    /*'semi': [
      'error',
      'always'
    ],*/
    'semi': 'off',
    /*'comma-dangle': [
      'error',
      'always-multiline'
    ],*/
    'comma-dangle': 'off',
    /*'no-console': ["error", { allow: ["warn", "error"] }],*/
    'no-console': 'off',
    // We need to exclude below for RegEx case
    "no-useless-escape": 0,
    'space-before-function-paren': 0,
    'indent': 'off',
    'no-unused-vars': 'off',
    'no-constant-condition': 'off',
  },
};
