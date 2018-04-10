__author__ = 'Adi Levin'

import vpython as visual
import winsound

class hanoi_move(object):

    def __init__(self,disk_to_move,from_rod,to_rod):
        self.disk_to_move = disk_to_move
        self.from_rod = from_rod
        self.to_rod = to_rod

    def __repr__(self):
        return 'Move disk #%i from rod %i to rod %i' % (self.disk_to_move,self.from_rod,self.to_rod)

class hanoi_graphics(object):

    def __init__(self,num_of_disks,num_of_rods):
        self.max_disk_radius = 1.0
        self.disk_thickness = 0.2
        self.rod_height = self.disk_thickness * (num_of_disks + 1)
        self.disks = [visual.cylinder(radius=self.max_disk_radius*(i+2)/(num_of_disks+1),
                                      length=self.disk_thickness,
                                      axis=visual.vector(0,0,1),
                                      color=visual.vector(0.0,0.5,1.0)) \
                      for i in range(num_of_disks)]
        self.rods  = [visual.cylinder(radius=self.max_disk_radius*1.0/(num_of_disks+1),
                                      color=visual.vector(1.0,0.5,0.3),
                                      length=self.rod_height,
                                      axis=visual.vector(0,0,1)) for i in range(num_of_rods)]
        for i in range(num_of_rods):
            self.rods[i].pos.x = self.max_disk_radius*2*(i-(num_of_rods-1)*0.5)
        for i in range(num_of_disks):
            self.set_disk_pos(disk=i,rod=0,z_order=num_of_disks-i-1)
        self.base = visual.box(
            pos=visual.vector(0,0,-self.disk_thickness*0.5),
            length=(num_of_rods+0.5)*self.max_disk_radius*2,
            width=self.disk_thickness,
            height=self.max_disk_radius*2.5,
            color=visual.vector(0.2,1.0,0.2))


    def set_disk_pos(self,disk,rod,z_order):
        self.disks[disk].pos.z = self.disk_thickness * z_order
        self.disks[disk].pos.x = self.rods[rod].pos.x

    def animate_disk_move(self,disk,to_rod,to_z_order):
        self.animate_motion_to_pos(self.disks[disk],visual.vector(self.disks[disk].pos.x,self.disks[disk].pos.y,self.rod_height + self.disk_thickness))
        self.animate_motion_to_pos(self.disks[disk],visual.vector(self.rods[to_rod].pos.x,self.rods[to_rod].pos.y,self.rod_height + self.disk_thickness))
        self.animate_motion_to_pos(self.disks[disk],visual.vector(self.rods[to_rod].pos.x,self.rods[to_rod].pos.y,self.disk_thickness * to_z_order))

    def animate_motion_to_pos(self,shape,new_pos):
        pos0 = shape.pos
        pos1 = new_pos
        num_steps = 30
        for i in range(num_steps):
            visual.rate(40)
            x = (i-1)*1.0/(num_steps-1)
            shape.pos = (1-x)*pos0 + x*pos1

def calc_hanoi_sequence(num_of_disks,from_rod,to_rod):

    if num_of_disks==0:
        return []
    l1 = calc_hanoi_sequence(num_of_disks=num_of_disks-1,from_rod=from_rod,to_rod=3-from_rod-to_rod)
    l2 = [hanoi_move(disk_to_move=num_of_disks-1,from_rod=from_rod,to_rod=to_rod)]
    l3 = calc_hanoi_sequence(num_of_disks=num_of_disks-1,from_rod=3-from_rod-to_rod,to_rod=to_rod)
    return l1+l2+l3

class hanoi_state(object):

    def __init__(self,num_of_disks):
        self.num_of_disks_per_rod = [num_of_disks,0,0]
        self.place_of_disk = [0]*num_of_disks

    def move_disk_to_rod(self,disk,to_rod):
        self.num_of_disks_per_rod[self.place_of_disk[disk]] -= 1
        self.place_of_disk[disk] = to_rod
        self.num_of_disks_per_rod[self.place_of_disk[disk]] += 1

def visualize_hanoi_solution(num_of_disks):
    g = hanoi_graphics(num_of_disks,3)
    state = hanoi_state(num_of_disks)

    def solve_one(from_rod,to_rod):
        moves = calc_hanoi_sequence(num_of_disks,from_rod,to_rod)
        visual.rate(1.0)
        for move in moves:
            winsound.Beep(880,50)
            g.animate_disk_move(disk=move.disk_to_move,to_rod=move.to_rod,to_z_order=state.num_of_disks_per_rod[move.to_rod])
            state.move_disk_to_rod(disk=move.disk_to_move,to_rod=move.to_rod)

    while True:
        solve_one(0,2)
        solve_one(2,0)

if __name__=='__main__':
    lights = [visual.distant_light(direction=visual.vector(0,ydir,0), color=visual.vector(1.0,1.0,1.0)) for ydir in [-1.0,1.0]]
    visualize_hanoi_solution(num_of_disks=6)
