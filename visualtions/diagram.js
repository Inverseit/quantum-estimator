const w = 800;
const h = 450;
const p = 20;
const step = 50;
const magic = Math.floor(h / step);
let data = null;
let paragraph = null;

// purely python habits
const print = (x) => {
  console.log(x);
};

const aps = [
  { x: p, y: h / 2 },
  { x: w / 2, y: p },
  { x: w - p, y: h / 2 },
  { x: w / 2, y: h - p },
];

const walls = [
  { x1: 0, y1: 0, x2: 0, y2: h },
  { x1: 0, y1: 0, x2: w, y2: 0 },
  { x1: w, y1: 0, x2: w, y2: h },
  { x1: w, y1: h, x2: 0, y2: h },
];

const drawWalls = () => {
  fill(0, 0, 0);
  strokeWeight(4);
  walls.forEach(({ x1, y1, x2, y2 }) => {
    line(x1, y1, x2, y2);
  });
};

const drawAps = () => {
  fill(255, 0, 0);
  strokeWeight(1);
  aps.forEach(({ x, y }) => {
    ellipse(x, y, 10, 10);
  });
};


function draw() {}

const predict = (vector) => {
  return { x: 0, y: 0 };
};

const calculateDiff = (x_ap, y_ap, x, y) => {
  const d = Math.sqrt(Math.pow(x_ap - x, 2) + Math.pow(y_ap - y, 2));
  return d;
};

const normalizeVector = (vector) => {
  norm = vector.map((x) => x * x).reduce((x, y) => x + y);
  return vector.map((x) => x / Math.sqrt(norm));
};

const calculateVector = (x, y) => {
  const res = [];
  for (const ap of aps) {
    const { x: x_ap, y: y_ap } = ap;
    const d = calculateDiff(x_ap, y_ap, x, y);
    res.push(d);
  }
  raw_norm_vector = normalizeVector(res);
  return normalizeVector(raw_norm_vector.map((l) => l - 0.5));
  // return raw_norm_vector;
};

const similarity = (v1, v2) => {
  score = 0;
  for (let index = 0; index < v1.length; index++) {
    score += v1[index] * v2[index];
  }
  return score * score;
};

const get_index = (x, y) => Math.floor(x / step) * magic + Math.floor(y / step);

const unget_index = (i) => {
  y = i % magic;
  x = Math.floor((i - y) / magic);
  return { x: x * step, y: y * step };
};

const train = () => {
  data_local = [];
  nts = [];
  for (let x = 0; x < w; x += step) {
    for (let y = 0; y < h; y += step) {
      data_local[get_index(x, y)] = calculateVector(x, y);
    }
  }
  return data_local;
};

const get_closest_index = (test_vector, visualize = false) => {
  let max = 0;
  let id = null;
  for (let index = 0; index < data.length; index++) {
    const train_vector = data[index];
    const sim = similarity(test_vector, train_vector);
    if (visualize) {
      const { x, y } = unget_index(index);
      fill(255 * (1 - sim));
      ellipse(x, y, 5, 5);
    }
    if (sim > max) {
      max = sim;
      id = index;
    }
  }
  return id;
};

const get_from_server = async (x, y) => {
  const t = calculateVector(x, y);
  try {
    const res = await fetch(
      `http://localhost:5000/localize?a=${t[0]}&b=${t[1]}&c=${t[2]}&d=${t[3]}`,
      {
        headers: {
          accept:
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        },
        method: "GET",
      }
    );
    return res;
  } catch (err) {
    console.log(err);
  }
};

async function mouseClicked() {
  paragraph.html("");

  fill(0, 255, 0);
  strokeWeight(1);
  const a = mouseX;
  const b = mouseY;

  console.log(a, b);

  ellipse(a, b, step / 2, step / 2);

  const test_vector = calculateVector(a, b);
  console.log(test_vector);
  const closest_index = get_closest_index(test_vector, (visualize = true));
  let { x, y } = unget_index(closest_index);
  console.log(x, y)

  const res = await get_from_server(a, b);
  let { x: x_s, y: y_s, confidence } = await res.json();

  const output = `Real (${a}, ${b}). Estimated (${x_s}, ${y_s}). Conf: ${confidence}`;
  paragraph.html(output);

  return false;
}


const test_draw = (x, y, fill) => {
  console.log("test");
  fill(0, 255, 0);
  strokeWeight(1);
  ellipse(x, y, step / 2, step / 2);
  const data = [{0: 0.48192056905749847, 1: 0.5848077126814282, 2: 0.5280982508373651, 3: 0.6257197696737045}, {4: 0.6587601940195086, 5: 0.7139043143955575, 6: 0.6883885629723587, 7: 0.7352339967724584}, {8: 0.741234146861345, 9: 0.4784934731435908, 10: 0.4304699128216032, 11: 0.5359316604378004}, {12: 0.6053465765004227, 13: 0.6764784443613441, 14: 0.6500828301180996, 15: 0.6987124463519313}, {16: 0.7177183562808995, 17: 0.33212069334474636, 18: 0.7243797481804175, 19: 0.4119096069401307}, {20: 0.48842230258541586, 21: 0.6063931806073521, 22: 0.5576669305885458, 23: 0.6536944237125493}, {24: 0.6667906680129669, 25: 0.675007952497084, 26: 0.695387761692051, 27: 0.2270010672358591}, {28: 0.31293817718291905, 29: 0.4784977830012287, 30: 0.3761614016458721, 31: 0.5631109678805457}, {32: 0.610091989886492, 33: 0.6334191334191335, 34: 0.6414120126448893, 35: 0.614970984400788}, {36: 0.11626191855871038, 37: 0.25815769765700225, 38: 0.17479522458375718, 39: 0.3427376099549453}, {40: 0.4565976887933352, 41: 0.5620103394979481, 42: 0.5271829549723608, 43: 0.5358703089636296}, {44: 0.49230932428131957, 45: 0.0454324455729026, 46: 0.025896308849229444, 47: 0.09993600682593862}, {48: 0.19478402607986955, 49: 0.3668964031875942, 50: 0.3027360066833751, 51: 0.38318054157172377}, {52: 0.36344750439460927, 53: 0.014933390631714616, 54: 0.31862331081081086, 55: 0.010874805807039145}, {56: 0.005697853985835222, 57: 0.1141460303964289, 58: 0.037005843027846486, 59: 0.16831467999565364}, {60: 0.17098501070663807, 61: 0.1275790371594605, 62: 0.17298767802848458, 63: 0.06441326530612246}, {64: 0.05098789037603568, 65: 0.00649943599935543, 66: 0.03413078149920257, 67: -0.0033608962389970465}, {68: 0.01735832932756498, 69: 0.029765068565961506, 70: 0.03121982619890573, 71: 0.03756442271930294}, {72: 0.19852311643835618, 73: 0.19268007234812212, 74: 0.17576407506702418, 75: 0.1607294317217981}, {76: 0.12246733322753, 77: 0.01692011137288496, 78: 0.059527626375975196, 79: 0.009996258085208765}, {80: -0.0004290924694272391, 81: 0.3713337615071719, 82: 0.327347112268211, 83: 0.412126677629834}, {84: 0.45864024164061257, 85: 0.30387267904509285, 86: 0.43251452016838066, 87: 0.155790838375108}, {88: 0.08700287877172408, 89: 0.5329602984279243, 90: 0.0305834796021488, 91: 0.6055900621118012}, {92: 0.6710827347698856, 93: 0.7358169238956892, 94: 0.7492904953145917, 95: 0.5832443970117396}, {96: 0.3981895633652822, 97: 0.1471313672922252, 98: 0.22812250332889483, 99: 0.7324820430965682}, {100: 0.8026644021017992, 101: 0.9327892462794047, 102: 0.8857081820123905, 103: 0.9059289383561644}, {104: 0.7844577103914628, 105: 0.43743625530087493, 106: 0.6158827901051067, 107: 0.3011180391313696}, {108: 0.8853482955748465, 109: 0.9824975840223343, 110: 0.9396266666666666, 111: 0.9944480034166133}, {112: 0.9553514206366162, 113: 0.7355877616747182, 114: 0.8606806199073335, 115: 0.5997668132916424}, {116: 0.4547286903941017, 117: 0.9847385272145144, 118: 0.9509684266383656, 119: 0.9964443486693244}, {120: 0.9764021164021164, 121: 0.861651901755875, 122: 0.9347149146354559, 123: 0.7820974064329056}, {124: 0.6783584895525595, 125: 0.9765785725589492, 126: 0.5779608983680724, 127: 0.9826077734768546}, {128: 0.9685875100509247, 129: 0.8872595898416746, 130: 0.9295955488979243, 131: 0.8332536774467634}, {132: 0.7843324829931972, 133: 0.6317331770472587, 134: 0.7125564109370852, 135: 0.9719052744886976}, {136: 0.9586998498176357, 137: 0.8886784511784511, 138: 0.9343629343629344, 139: 0.8401069518716577}, {140: 0.8032560852733732, 141: 0.733326219186853, 142: 0.7774693005872931, 143: 0.6692196454394516}]
  data.forEach(sample => {
    for (const k in sample) {
      if (Object.hasOwnProperty.call(sample, k)) {
        const sim = sample[k];
        const { x, y } = unget_index(k);
        fill(255 * (1 - sim));
        ellipse(x, y, 5, 5);
      }
    }
  })
}

function setup() {
  createCanvas(w, h);
  background(228);
  drawWalls();
  drawAps();
  paragraph = createP("Welcome to the estimator");
  paragraph.style("font-size", "48px");
  paragraph.style("margin-top", "10px");
  paragraph.position(10, 0);
  data = train();

  // test_draw(622, 120, fill);
}