import React, { useCallback, useEffect, useState } from 'react';
import ReactFlow, { Handle, Node, Edge, Background, getIncomers } from 'react-flow-renderer';
import { useParams } from 'react-router-dom';
import axios from 'axios'
import dagre from 'dagre';

import NoPage from './NoPage';
import Legend from '../components/graph/Legend'
import CourseNode from '../components/graph/CourseNode'

import '../styles/graph.css'
import { Button, OverlayTrigger, Popover } from 'react-bootstrap'

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
  const nodeTypes = { courseNode: CourseNode };

  const getNode = (course) => {
    for(let i = 0; i < Object.keys(nodes).length; i++){
      //console.log(nodes[i].id);
      if(course.localeCompare(nodes[i].id) === 0){
        return nodes[i];
      }
    }
  }
  
  const updateDrop = (course, count) => {
    console.log(nodes)
    let droppedCourseNode = getNode(course);
    
    let unavailableCourses = [];
    let visited = new Set();
    let q = [droppedCourseNode];

    while (q.length > 0) {
      let currentNode = q.shift()
      unavailableCourses.push(currentNode.id)

      let incomingNodes = getIncomers(currentNode, nodes, edges)
      incomingNodes.forEach(node => {
        if (!visited.has(node.id)) {
          visited.add(node.id)
          q.push(node)
        } 
      })
    }

    setNodes(nodes.map(node => {
      if (unavailableCourses.includes(node.id)) {
        node.data.dropValue += count;
      }
      return node;
    }))
  }
  // useEffect(() => {
  // }, [nodes, edges])


  useEffect(() => {

    const getGraph = () => {
      let request_url = "";

      if (typeof params.minor !== 'undefined') {
        request_url = global.config.base_url + '/graph/' + params.type + "/"+ params.minor + "/" + params.code;
      } else {
        request_url = global.config.base_url + '/graph/' + params.type + '/' + params.code;
      }

      axios.get(request_url).then((res) => {
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
              updateDrop: updateDrop
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
        {/* <Button onClick={() => {console.log(nodes)}}>test</Button> */}
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
