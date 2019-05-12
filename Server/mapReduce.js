//count the fastfood related tweets for each region
function (doc) {
  if (doc.alcohols_score > 0 && doc.region != null && doc.label == 1){
      emit(doc.region, [1,0,1]);
  }else if (doc.alcohols_score > 0 && doc.region != null && doc.label == 0){
      emit(doc.region, [0,1,1]);
  }else if (doc.region != null){
      emit(doc.region, [0,0,1]);
  }
}
function (keys, values, rereduce) {
  var result = {total: 0, num : 0, pos_count : 0, neg_count : 0, nagative_portion:0, positive_portion:0};
  for(i=0; i < values.length; i++) {
    if(rereduce) {
        result.total = result.total + values[i].total;
        result.pos_count = result.pos_count + values[i].pos_count;
        result.neg_count = result.neg_count + values[i].neg_count;
        result.num = result.pos_count + result.neg_count
        result.positive_portion = result.pos_count / result.total
        result.nagative_portion = result.neg_count / result.total

    } else {
        result.total = values.length;
        for(i=0; i < values.length; i++) {
           result.pos_count = result.pos_count + values[i][0]
           result.neg_count = result.neg_count + values[i][1]
        }
        result.num = result.pos_count + result.neg_count
        result.positive_portion = result.pos_count / result.total
        result.nagative_portion = result.neg_count / result.total
    }
  }
  return(result);
}

//count the fastfood related tweets for each region
function (doc) {
  if (doc.fastfood_score > 0 && doc.region != null && doc.label == 1){
      emit(doc.region, [1,0,1]);
  }else if (doc.fastfood_score > 0 && doc.region != null && doc.label == 0){
      emit(doc.region, [0,1,1]);
  }else if (doc.region != null){
      emit(doc.region, [0,0,1]);
  }
}

function (keys, values, rereduce) {
  var result = {total: 0, pos_count : 0, neg_count : 0, nagative_portion:0, positive_portion:0};
  for(i=0; i < values.length; i++) {
    if(rereduce) {
        result.total = result.total + values[i].total;
        result.pos_count = result.pos_count + values[i].pos_count;
        result.neg_count = result.neg_count + values[i].neg_count;
        result.positive_portion = result.pos_count / result.total
        result.nagative_portion = result.neg_count / result.total

    } else {
        result.total = values.length;
        for(i=0; i < values.length; i++) {
           result.pos_count = result.pos_count + values[i][0]
           result.neg_count = result.neg_count + values[i][1]
        }
        result.positive_portion = result.pos_count / result.total
        result.nagative_portion = result.neg_count / result.total
    }
  }
  return(result);
}

//count the smoking related tweets for each region
function (doc) {
  if (doc.smoking_score > 0 && doc.region != null && doc.label == 1){
      emit(doc.region, [1,0,1]);
  }else if (doc.smoking_score > 0 && doc.region != null && doc.label == 0){
      emit(doc.region, [0,1,1]);
  }else if (doc.region != null){
      emit(doc.region, [0,0,1]);
  }
}

function (keys, values, rereduce) {
  var result = {total: 0, num : 0, pos_count : 0, neg_count : 0, nagative_portion:0, positive_portion:0};
  for(i=0; i < values.length; i++) {
    if(rereduce) {
        result.total = result.total + values[i].total;
        result.pos_count = result.pos_count + values[i].pos_count;
        result.neg_count = result.neg_count + values[i].neg_count;
        result.num = result.pos_count + result.neg_count
        result.positive_portion = result.pos_count / result.total
        result.nagative_portion = result.neg_count / result.total

    } else {
        result.total = values.length;
        for(i=0; i < values.length; i++) {
           result.pos_count = result.pos_count + values[i][0]
           result.neg_count = result.neg_count + values[i][1]
        }
        result.num = result.pos_count + result.neg_count
        result.positive_portion = result.pos_count / result.total
        result.nagative_portion = result.neg_count / result.total
    }
  }
  return(result);
}

//count the positive/negative tweets for each region
function (doc) {
  if (doc.label == 1 && doc.region != null){
      emit(doc.region, [1, 0]);
  }else if (doc.label == 0 && doc.region != null){
      emit(doc.region, [0, 1]);
  }
}

function (keys, values, rereduce) {
  var result = {pos_count : 0, neg_count : 0};
  for(i=0; i < values.length; i++) {
    if(rereduce) {
        result.pos_count = result.pos_count + values[i].pos_count;
        result.neg_count = result.neg_count + values[i].neg_count;
    } else {
        result.total = values.length;
        for(i=0; i < values.length; i++) {
           result.pos_count = result.pos_count + values[i][0]
           result.neg_count = result.neg_count + values[i][1]
        }
    }
  }
  return(result);
}


function (doc) {
  if (doc.alcohols_score > 0){
      emit("alcohol", 1);
  }else if (doc.smoking_score > 0){
      emit("smoking", 1);
  }else if (doc.fastfood_score > 0){
      emit("fastfood", 1);
  }
}

function (keys, values, rereduce) {
  if (rereduce) {
    return sum(values);
  } else {
    return values.length;
  }
}