class Message:
    def __init__(self, event_time, msg_size, vertex_id, accumulated_latency=0.0):
        self._msg_size = msg_size
        self._vertex_id = vertex_id
        self._event_time = event_time
        self._transmission_delay = None
        self._accumulated_latency = accumulated_latency
        self._queuein_time = None
        self._e2e_delay = 0
        self._rcv_time = 0
        #self._response_time = 0
        
    def __str__(self):
        return f'{self._vertex_id} {self._event_time}, {self._rcv_time}'
    
    @property
    def msg_size(self):
        return self._msg_size
    
    @property
    def vertex_id(self):
        return self._vertex_id
    
    @property
    def event_time(self):
        return self._event_time
    
    @property
    def transmission_delay(self):
        return self._transmission_delay
    
    @property
    def accumulated_latency(self):
        return self._accumulated_latency
    
    @property
    def queuein_time(self):
        return self._queuein_time
    
    @property
    def rcv_time(self):
        return self._rcv_time
    
    def update_transmission_delay(self, transmission_delay):
        if transmission_delay <= 0:
            print('Delay must be over than 0.0')
            return
        
        self._transmission_delay = transmission_delay
        
    def update_accumulated_latency(self, latency):
        if latency <= 0:
            print('Delay must be over than 0.0')
            return
        
        self._accumulated_latency += latency
        
    def update_queuein_time(self, time):
        self._queuein_time = time
    
    def update_receive_time(self, time):
        self._rcv_time = time
        