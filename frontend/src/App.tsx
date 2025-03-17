import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';        // Core grid CSS
import 'ag-grid-community/styles/ag-theme-alpine.css'; // Optional theme, e.g. Alpine

const App: React.FC = () => {
  const columnDefs = [  // define grid columns
    { field: 'name', headerName: 'Name' },
    { field: 'age', headerName: 'Age' }
  ];
  const rowData = [     // define some row data
    { name: 'Alice', age: 25 },
    { name: 'Bob', age: 30 }
  ];

  return (
    <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
      <AgGridReact columnDefs={columnDefs} rowData={rowData} />
    </div>
  );
};

export default App;
