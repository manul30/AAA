
import { PieChart, Pie, Sector, Cell, ResponsiveContainer } from 'recharts';

const data = [
    { name: "Insatisfecho", value: 200 },
    { name: "Neutral", value: 300 },
    { name: "Molesto", value: 100 },
    { name: "Feliz", value: 600 }
  ];
  const COLORS = ["#C92416", "#009BF3", "#B54AF6", "#2FC5A1"];

const PieComponent  = () => (
    <PieChart width={800} height={400}>
      <Pie
        data={data}
        cx={120}
        cy={200}
        innerRadius={60}
        outerRadius={80}
        fill="#8884d8"
        paddingAngle={5}
        dataKey="value"
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
      <Pie
        data={data}
        cx={420}
        cy={200}
        startAngle={180}
        endAngle={0}
        innerRadius={60}
        outerRadius={80}
        fill="#8884d8"
        paddingAngle={5}
        dataKey="value"
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
    </PieChart>
  
);

function Piechart(){
    return (
        <div>
            <PieComponent></PieComponent>
        </div>
    );
}

export default Piechart;