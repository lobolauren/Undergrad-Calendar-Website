import { useEffect, useState } from 'react';
import ReactFlow, { Background, getIncomers, getOutgoers, getConnectedEdges } from 'react-flow-renderer';
import { useParams } from 'react-router-dom';
import axios from 'axios'
import dagre from 'dagre';

import NoPage from './NoPage';
import Legend from '../components/graph/Legend'
import CourseNode from '../components/graph/CourseNode'

import '../styles/graph.css'

// Clear potential course name from home search
localStorage.clear();

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 120;
const nodeHeight = 38;

const getLayoutedElements = (nodes, edges, direction = 'TB') => {
  const isHorizontal = direction === 'LR';
  dagreGraph.setGraph({ rankdir: direction, ranksep: 150, nodesep: 50 });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  nodes.forEach((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    node.targetPosition = isHorizontal ? 'left' : 'top';
    node.sourcePosition = isHorizontal ? 'right' : 'bottom';

    node.position = {
      x: nodeWithPosition.x - nodeWidth / 2,
      y: nodeWithPosition.y - nodeHeight / 2,
    };

    return node;
  });

  return { nodes, edges };
};

const Graph = () => {
  
  const params = useParams();
  
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [receivedRequest, setReceivedRequest] = useState(false);
  
  const getNode = (course) => {
    return nodes.filter(node => node.id === course)[0];
  }

  const simulateDrop = (course) => {
    console.log(course)
    // console.log(nodes)
    console.log(getNode(course))
    let result = getOutgoers(getNode(course), nodes, edges)
    console.log(result)
  }

  const nodeTypes = { courseNode: CourseNode };

  useEffect(() => {
    const getGraph = () => {
      let checkMinor = "";

      if (typeof params.minor !== 'undefined') {
        checkMinor = global.config.base_url + '/graph/' + params.type + "/"+ params.minor + "/" + params.code;
      } else {
        checkMinor = global.config.base_url + '/graph/' + params.type + '/' + params.code;
      }

      axios.get(checkMinor).then((res) => {
        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
          res.data.nodes,
          res.data.edges,
          'LR'
        );

        setNodes([...layoutedNodes.map((node) => {
          return {
            ...node,
            data: {
              ...node.data,
              simulateDrop: simulateDrop
            },
          }
        })]);
        setEdges([...layoutedEdges]);
        setReceivedRequest(true)
      });
    }
    getGraph();  
  }, [params])

  return <div>
    {receivedRequest === false || nodes.length > 0
    ? <div className='reactflow-container'>
        <Legend />

        <ReactFlow 
          nodes={nodes} 
          edges={edges} 
          nodeTypes={nodeTypes}
          fitView 
        >
          <Background color="#aaa" gap={15} size={0.6} />
        </ReactFlow>
      </div>
    : <NoPage />}
  </div>
}

export default Graph;