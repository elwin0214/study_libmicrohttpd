### 介绍

```shell
代码来自 libmicrohttpd-0.9.5 分离出主要代码使用 cmake管理 
项目站点 ： https://www.gnu.org/software/libmicrohttpd/

mkdir build
cd build
cmake  -DCMAKE_BUILD_TYPE=Debug/Release ..
```

### 主要函数
* 1.MHD_start_daemon_va()：启动服务。
```
如果满足以下2种任意一个
1.MHD_USE_THREAD_PER_CONNECTION   
2.MHD_USE_SELECT_INTERNALLY && daemon.worker_pool_size==0 
创建线程调用 MHD_select_thread

根据daemon.worker_pool_size 创建对应数量的线程，线程调用MHD_select_thread
```

* 2.MHD_select_thread(struct MHD_Daemon *daemon)：线程执行主体。
```
在 MHD_YES != daemon->shutdown 情况下循环执行如下操作：
如果指定了 MHD_USE_POLL 则调用 MHD_poll (daemon, MHD_YES);// 内部类似 MHD_select
否则调用 MHD_select (daemon, MHD_YES);
MHD_cleanup_connections (daemon);
```

* 3.MHD_select (struct MHD_Daemon *daemon, int may_block)
```
收集要关注的fd：
如果指定了 MHD_USE_THREAD_PER_CONNECTION 则只关注 daemon->socket_fd；
否则还关注 daemon上的connection对应的fd；
调用select获取到事件后调用 
MHD_run_from_select (struct MHD_Daemon *daemon, const fd_set *read_fd_set, const fd_set *write_fd_set, const fd_set *except_fd_set)
```

* 4.MHD_run_from_select()
```
如果daemon上的 socket_fd 有读事件 则调用 MHD_accept_connection (daemon);
如果没有指定  MHD_USE_THREAD_PER_CONNECTION 则对所有 daemon上的连接调用 call_handlers()  
```

* 5.MHD_accept_connection()
```
对damon->socket_fd调用
如果daemon->work_pool_size>0 调用 internal_add_connection  将连接添加到daemon的各个线程池中(子daemon)
否则添加到daemon 连接队列中，如果指定了MHD_USE_THREAD_PER_CONNECTION创建线程调用 MHD_handle_connection()
```

### 主要模式

* Thread Per Connection 

参数：MHD_USE_THREAD_PER_CONNECTION    
单独创建线程处理accept连接，对accept到的每个连接创建一个独立的线程处理读写。

* Internal

参数：worker_pool_size == 0 && MHD_USE_SELECT_INTERNALLY
单独创建线程处理accept连接，以及连接的读写。

* Thread pool

参数：worker_pool_size>0 && MHD_USE_SELECT_INTERNALLY
创建worker_pool_size （只有在这种情况下大于0 ）个线程，每个线程都会accept连接，并且处理连接的读写。




### Question

* 连接超时以及关闭

如果设置了`MHD_USE_THREAD_PER_CONNECTION` 每个连接创建线程调用 `MHD_handle_connection()`处理当前连接，
内部会对连接循环调用`call_handlers()`内部会调用 `MHD_connection_handle_idle()`

```c
MHD_handle_connection (void *data)
->call_handlers (struct MHD_Connection *con, int read_ready, int write_ready, int force_close)
  -> MHD_connection_handle_idle (struct MHD_Connection *connection)
    -> 如果超时 调用 MHD_connection_close_() 设置连接状态为 MHD_CONNECTION_CLOSED ，并return MHD_YES;
-> 上面返回的 MHD_YES 导致 进入到exit 代码块 
  -> shutdown (con->socket_fd, SHUT_WR);
  -> MHD_socket_close_ (con->socket_fd);  // 关闭fd
```

如果是其他的情况，以`MHD_select_thread()`为例，在循环体里面会调用
```c
MHD_select_thread()
->MHD_select (daemon, MHD_YES);
  ->MHD_run_from_select()
   -> call_handlers()
     ->MHD_connection_handle_idle (struct MHD_Connection *connection)
       内部会处理超时设置状态为 MHD_CONNECTION_CLOSED ，
       同时在 MHD_CONNECTION_CLOSED 状态下会调用  cleanup_connection (connection); 添加到cleanup 队列
->MHD_cleanup_connections (daemon); //会对 cleanup 中的conn 调用 MHD_socket_close_
```
  
MHD_Connection  
read_closed：MHD_YES表示client关闭，或者按照协议，应该关闭连接。


