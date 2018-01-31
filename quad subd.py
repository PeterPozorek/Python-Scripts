import Rhino.Geometry as rg

def subdivide(mesh, recursion, offset1, offset2):
    mesh2 = rg.Mesh()
    
    vtx = mesh.Vertices.ToPoint3dArray()
    for i in range(len(vtx)):
        vtx2 = vtx[i] + rg.Vector3d(mesh.Normals[i]) * offset1 # offset vertex
        mesh2.Vertices.Add(vtx2)
    
    for i in range(mesh.Faces.Count):
        if(mesh.Faces[i].IsQuad): # quad face
            vidx1 = mesh.Faces[i].A
            vidx2 = mesh.Faces[i].B
            vidx3 = mesh.Faces[i].C
            vidx4 = mesh.Faces[i].D
            
            v1 = vtx[vidx1]
            v2 = vtx[vidx2]
            v3 = vtx[vidx3]
            v4 = vtx[vidx4]
            
            w1 = (v1+v2)/2 # mid point
            w2 = (v2+v3)/2 # mid point
            w3 = (v3+v4)/2 # mid point
            w4 = (v4+v1)/2 # mid point
            w5 = (v1+v2+v3+v4)/4 # center
            w5 += rg.Vector3d(mesh.FaceNormals[i]) * offset2 #offset new vertex
            
            widx1 = mesh2.Vertices.Add(w1)
            widx2 = mesh2.Vertices.Add(w2)
            widx3 = mesh2.Vertices.Add(w3)
            widx4 = mesh2.Vertices.Add(w4)
            widx5 = mesh2.Vertices.Add(w5)
            mesh2.Faces.AddFace(vidx1,widx1,widx5,widx4)
            mesh2.Faces.AddFace(vidx2,widx2,widx5,widx1)
            mesh2.Faces.AddFace(vidx3,widx3,widx5,widx2)
            mesh2.Faces.AddFace(vidx4,widx4,widx5,widx3)
            
        else: # triangular face
            mesh2.Faces.AddFace(mesh.Faces[i])
    
    mesh2.Normals.ComputeNormals()
    mesh2.Weld(180) #weld vertices
    if(recursion>1):
        return subdivide(mesh2, recursion-1, offset1/2, offset2/2)
    return mesh2

a = subdivide(mesh, recursionLevel, offsetDepth1, offsetDepth2)
