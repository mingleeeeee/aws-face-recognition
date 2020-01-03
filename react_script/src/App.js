import React, {useEffect, useState} from 'react';
import './App.css';
import Amplify, { I18n } from 'aws-amplify';
import awsconfig from './aws-exports';
import { withAuthenticator } from 'aws-amplify-react';
import { Table } from 'antd';

Amplify.configure(awsconfig);
I18n.setLanguage('en');

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    getData().then(data => {
      setData(data)
    })
  }, []);
  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      // specify the condition of filtering result
      // here is that finding the name started with `value`
      onFilter: (value, record) => record.name.indexOf(value) === 0,
      sorter: (a, b) => a.name.length - b.name.length,
      sortDirections: ['descend'],
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      defaultSortOrder: 'descend',
      sorter: (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
    }
  ];
  
  const dataTable = data
  
  function onChange(pagination, filters, sorter, extra) {
    console.log('params', pagination, filters, sorter, extra);
  }
  
  return (
<Table columns={columns} dataSource={dataTable} onChange={onChange} />
  );
}

export default withAuthenticator(App, true);

function getData() {
  return new Promise((resolve, reject) => {
    fetch('Your-API-Gatway-Endpoint', {
      method: "GET"
    }).then(response => response.json()).then(data => {
      const response = data.body.map((item, index)=>({
        "name": item.name.S,
        "timestamp": item.timestamp.S,
        "key": index
      }))
      console.log('response',response)
      resolve(response)})
  })
  
}