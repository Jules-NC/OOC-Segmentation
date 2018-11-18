 class Block:
  def __init__(self, block_index = 0, pixel_ini =(0, 0), pixel_end = (0, 0)):
    self.block_index = block_index
    self.pixel_ini.x = pixel_ini[0]
    self.pixel_ini.y = pixel_ini[1]
    self.pixel_end.x = pixel_end[0]
    self.pixel_end.y = pixel_end[1]

    #size of the block

    self.lenght = self.pixel_end.x - self.pixel_ini.x
    self.height = self.pixel_end.y - self.pixel_ini.y
    self.area = self.lenght * self.height

    #read image // random img
    imsize.len_x = self.lenght
    imsize.len_y = self.height

    self.block_graph = generate_graph(imsize)

    #define edges and weights


    #define QBT
    self.block_tree = do_QBT(self.block_graph, imsize)
  #return the index of the block
  # don't know if this is necessary
  def blockIndex(self)
   return self.block_index
  def boundaryOf(leaf = (0, 0)):
    # return the boundary tree of this pixel/leaf
    self.boundary = None

    #search for all node parents of this leaf
    #and add them to the boundary
    
    return self.boundary
