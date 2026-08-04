// VC Deal Flow Signal — Product API
// GET /api/product — Returns product catalog with pricing

const products = [
  {
    id: 'monthly-data',
    name: 'Monthly Data — VC Deal Flow Signal',
    price: 3.00,
    currency: 'USD',
    interval: 'month',
    description: 'Full dataset export of 324+ startups + last 4 weeks of velocity signals. CSV/JSON format.',
    features: [
      'Complete CSV/JSON export of 324+ startups',
      '4 weeks of historical velocity data',
      'Sector classification + velocity trends',
      'Contributor breakdown by startup',
      'Signal type analysis (hiring bursts, deploy spikes, infra buildouts, framework migrations)'
    ],
    stripe_link: 'https://buy.stripe.com/test_XXXXXXXX',
    popular: false
  },
  {
    id: 'annual-premium',
    name: 'Annual Premium — VC Deal Flow Signal',
    price: 29.00,
    currency: 'USD',
    interval: 'year',
    description: 'Everything in Monthly + full historical dataset + priority support + early access to new signal types.',
    features: [
      'Full dataset + historical trends archive',
      '52 weeks of historical velocity data',
      'Priority email support within 12 hours',
      'Early access to new signal types',
      'SSRN research methodology reference'
    ],
    stripe_link: 'https://buy.stripe.com/test_YYYYYYYY',
    popular: true
  }
];

export default function handler(req, res) {
  const origin = req.headers.origin || '*';

  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  res.setHeader('Content-Type', 'application/json');
  return res.status(200).json({ products });
}
