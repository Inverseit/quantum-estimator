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
}

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
