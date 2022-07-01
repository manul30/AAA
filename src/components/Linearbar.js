import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
const data = 
[
    {name: '15 May', uv: 32, pv: 2400, amt: 2400},
    {name: '16 May', uv: 18, pv: 2400, amt: 2400},
    {name: '17 May', uv: 8, pv: 2400, amt: 2400},
    {name: '18 May', uv: 41, pv: 2400, amt: 2400},
    {name: '19 May', uv: 47, pv: 2400, amt: 2400},
    {name: '20 May', uv: 14, pv: 2400, amt: 2400},
    {name: '21 May', uv: 3, pv: 2400, amt: 2400}
];

const RenderLineChart  = () => (
  <LineChart width={900} height={300} data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
    <Line type="monotone" dataKey="uv" stroke="#2A26E2" strokeWidth={3}/>
    <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip />
  </LineChart>
);

function Linearbar(){
    return (
        <div>
            <RenderLineChart></RenderLineChart>
        </div>
    );
}

export default Linearbar;