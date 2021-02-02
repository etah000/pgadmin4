/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2020, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

import _ from 'underscore';

function generate_url(baseUrl, treeInfo, actionType, nodeType, pickFunction, itemDataID) {
  console.log(baseUrl);
  console.log(treeInfo);
  console.log(actionType);
  console.log(nodeType);

  let ref = '';
  _.each(
    _.sortBy(
      _.pick(treeInfo, pickFunction),
      function (treeInfoItems) {
        return treeInfoItems.priority;
      }
    ),
    function (treeInfoItems) {
      ref = `${ref}/${encodeURI(treeInfoItems._id)}`;
    }
  );
  ref = itemDataID ? `${ref}/${itemDataID}` : `${ref}/`;

  return `${baseUrl}${nodeType}/${actionType}${ref}`;
}

module.exports = {
  generate_url: generate_url,
};
